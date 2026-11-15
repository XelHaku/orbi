"""Experiment A collector. Derived from the pilot collector (subscription-pilot/openrouter-v1/source/accounting.py).
Changes: each sampled process row also carries its own comm and utime/stime ticks, so the agent (root)
process can be separated from tool children; the pilot's fixed 0.02 ms CPU gate is recorded, not fatal,
beside the timeval-resolution bound 2*(N+1) microseconds.

Linux child-subreaper accounting: wait4 subtree CPU and sampled simultaneous tree PSS.

One fresh supervisor per observation. No other child is started by this supervisor.
The fake server and experiment driver are ancestors/siblings, never charged to the agent.
Memory is sampled, not an exact kernel-maintained PSS high-water mark.
"""
import ctypes
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import threading
import time


def parse_stat(text):
    end = text.rfind(')')
    fields = text[end + 2:].split()
    return {'pid': int(text.split(' ', 1)[0]), 'comm': text[text.find('(')+1:end], 'ppid': int(fields[1]),
            'state': fields[0], 'start_ticks': int(fields[19]),
            'utime_ticks': int(fields[11]), 'stime_ticks': int(fields[12])}


def parse_memory(text):
    fields = {}
    for line in text.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key] = int(value.strip().split()[0])
    required = {'Pss', 'Private_Clean', 'Private_Dirty', 'Private_Hugetlb'}
    if not required <= fields.keys():
        raise ValueError(f'missing memory fields: {required - fields.keys()}')
    return {'pss_kib': fields['Pss'], 'private_kib': sum(fields[k] for k in required if k != 'Pss')}


def descendants(table, parent):
    found = set()
    parents = {parent}
    while parents:
        children = {pid for pid, data in table.items() if data['ppid'] in parents and pid not in found}
        found |= children
        parents = children
    return found


def snapshot(supervisor):
    table = {}
    races = []
    for path in Path('/proc').iterdir():
        if not path.name.isdigit():
            continue
        try:
            value = parse_stat((path / 'stat').read_text())
            table[value['pid']] = value
        except (FileNotFoundError, ProcessLookupError):
            pass  # A process ended during discovery; CPU is retained by wait4.
    rows = []
    for pid in sorted(descendants(table, supervisor)):
        before = table[pid]
        if before['state'] in ('Z', 'X'):
            continue
        base = Path('/proc') / str(pid)
        try:
            data = (base / 'smaps_rollup').read_text()
            after = parse_stat((base / 'stat').read_text())
            if after['start_ticks'] != before['start_ticks'] or after['state'] in ('Z', 'X'):
                races.append(pid)
                continue
            rows.append({**before, **parse_memory(data)})
        except (FileNotFoundError, ProcessLookupError):
            races.append(pid)
    return rows, races


def collect(config):
    out = Path(config['out'])
    out.mkdir(parents=True, exist_ok=False)
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER, no privileges required.
        raise OSError(ctypes.get_errno(), 'cannot enable child subreaper')
    own_before = time.process_time()
    reaped = []
    samples = []
    failures = []
    complete = threading.Event()
    root_exit = []
    start = time.perf_counter()
    with (out / 'stdout.bin').open('wb') as stdout, (out / 'stderr.bin').open('wb') as stderr:
        proc = subprocess.Popen(config['argv'], env=config['env'], cwd=config['cwd'],
                                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, start_new_session=True)
        def reap():
            try:
                while True:
                    try:
                        pid, status, ru = os.wait4(-1, 0)
                    except ChildProcessError:
                        break
                    at = time.perf_counter()
                    code = os.waitstatus_to_exitcode(status)
                    reaped.append({'pid': pid, 'exit': code, 'at_ms': (at-start)*1000,
                                   'user_ms': ru.ru_utime*1000, 'system_ms': ru.ru_stime*1000,
                                   'wait4_peak_rss_kib': ru.ru_maxrss})
                    if pid == proc.pid:
                        proc.returncode = code
                        root_exit.append(at)
            except BaseException as exc:
                failures.append(f'reaper: {exc!r}')
            finally:
                complete.set()
        waiter = threading.Thread(target=reap, daemon=True)
        waiter.start()
        interval = config.get('sample_interval_s', 0.002)
        timed_out = False
        while not complete.is_set():
            tick = time.perf_counter()
            if tick - start > config.get('timeout_s', 90):
                timed_out = True
                failures.append('measurement deadline exceeded')
                # Only this observation's process group, within the isolated container.
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                break
            if config.get('sample_memory', True):
                try:
                    rows, races = snapshot(os.getpid())
                    samples.append({'at_ms': (tick-start)*1000, 'scan_ms': (time.perf_counter()-tick)*1000,
                                    'processes': rows, 'exit_races': races,
                                    'tree_pss_kib': sum(r['pss_kib'] for r in rows),
                                    'tree_private_kib': sum(r['private_kib'] for r in rows)})
                except BaseException as exc:
                    failures.append(f'sampler: {exc!r}')
                    # Finish/reap this bounded observation; never run the next one.
                    break
            complete.wait(max(0, interval-(time.perf_counter()-tick)))
        waiter.join(timeout=5 if timed_out else config.get('timeout_s', 90))
        if waiter.is_alive():
            failures.append('descendants still alive after measurement bound')
        finish = time.perf_counter()
    root_rows = [r for r in reaped if r['pid'] == proc.pid]
    observed = {(p['pid'], p['start_ticks']) for s in samples for p in s['processes']}
    positive = [s for s in samples if s['tree_pss_kib'] > 0]
    if not root_rows or len(root_exit) != 1:
        failures.append('missing root exit')
    if config.get('sample_memory', True) and not positive:
        failures.append('no live positive PSS samples')
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu_ms = sum(r['user_ms']+r['system_ms'] for r in reaped)
    # A fresh supervisor: independent aggregate check against all reaped children.
    aggregate_ms = (children.ru_utime+children.ru_stime)*1000
    cpu_gap_us = abs(cpu_ms-aggregate_ms)*1000
    original_cpu_gate_passed = cpu_gap_us <= 20
    resolution_bound_us = 2*(len(reaped)+1)
    if cpu_gap_us > resolution_bound_us:
        failures.append(f'wait4 vs RUSAGE_CHILDREN beyond resolution bound: {cpu_ms} vs {aggregate_ms}')
    tick_ms = 1000/os.sysconf('SC_CLK_TCK')
    root_rows_sampled = [p for s in samples for p in s['processes'] if p['pid'] == proc.pid]
    child_pss = [sum(p['pss_kib'] for p in s['processes'] if p['pid'] != proc.pid) for s in samples]
    comms = sorted({p['comm'] for s in samples for p in s['processes'] if p['pid'] != proc.pid})
    gaps = [b['at_ms']-a['at_ms'] for a, b in zip(samples, samples[1:])]
    result = {'argv': config['argv'], 'cwd': config['cwd'], 'root_pid': proc.pid,
              'ok': not failures and bool(root_rows) and root_rows[0]['exit'] == 0,
              'failures': failures, 'reaped': reaped,
              'wall_ms': ((root_exit[0] if root_exit else finish)-start)*1000,
              'tree_lifetime_wall_ms': (finish-start)*1000,
              'tree_cpu_ms': cpu_ms, 'rusage_children_cpu_ms': aggregate_ms,
              'observer_cpu_ms': (time.process_time()-own_before)*1000,
              'peak_tree_pss_mib': max((s['tree_pss_kib'] for s in samples), default=0)/1024,
              'peak_tree_private_mib': max((s['tree_private_kib'] for s in samples), default=0)/1024,
              'sample_count': len(samples), 'positive_sample_count': len(positive),
              'observed_processes': sorted(observed), 'sample_interval_ms': interval*1000,
              'max_sample_gap_ms': max(gaps, default=0), 'samples_file': str(out/'samples.jsonl'),
              'sample_memory': config.get('sample_memory', True),
              'original_cpu_gate_passed': original_cpu_gate_passed, 'cpu_gap_us': cpu_gap_us,
              'resolution_bound_us': resolution_bound_us,
              'agent_comm': root_rows_sampled[-1]['comm'] if root_rows_sampled else None,
              'agent_cpu_ms_last_sample': (root_rows_sampled[-1]['utime_ticks']+root_rows_sampled[-1]['stime_ticks'])*tick_ms if root_rows_sampled else None,
              'agent_last_sample_before_exit_ms': (root_exit[0]-start)*1000-[s['at_ms'] for s in samples if any(p['pid']==proc.pid for p in s['processes'])][-1] if root_rows_sampled and root_exit else None,
              'agent_peak_pss_mib': max((p['pss_kib'] for p in root_rows_sampled), default=0)/1024,
              'agent_peak_private_mib': max((p['private_kib'] for p in root_rows_sampled), default=0)/1024,
              'children_peak_pss_mib': max(child_pss, default=0)/1024, 'child_comms': comms,
              'agent_pss_series_mib': [[round(s['at_ms']), round(p['pss_kib']/1024, 1)] for s in samples for p in s['processes'] if p['pid'] == proc.pid][::20]}
    (out/'samples.jsonl').write_text(''.join(json.dumps(s)+'\n' for s in samples))
    (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    if not result['ok']:
        raise SystemExit(1)


if __name__ == '__main__':
    collect(json.loads(Path(sys.argv[1]).read_text()))
