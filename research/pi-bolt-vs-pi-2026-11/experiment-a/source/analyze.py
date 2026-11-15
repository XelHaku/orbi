"""Summarize the fixed replay schedule: one row per launch, medians and ranges per trace and executable, paired differences."""
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fidelity

ROOT = Path(__file__).resolve().parent.parent
PILOT = ROOT.parent / 'subscription-pilot/openrouter-v1/results/coding-pair'
TRACES = {'pitrace': (PILOT / 'relay', PILOT / 'standard-pi/delivery-manifest.json'),
          'bolttrace': (PILOT / 'pi-bolt/relay', PILOT / 'pi-bolt/delivery-manifest.json')}
METRICS = ['wall_s', 'tree_cpu_s', 'agent_cpu_s', 'agent_peak_pss_mib', 'tree_peak_pss_mib', 'children_peak_pss_mib', 'non_fixture_wall_s']
rows = []
for spec in json.loads((ROOT / 'schedule.json').read_text())['pairs']:
    recorded = fidelity.load(TRACES[spec['trace']][0])
    delivery = json.loads(TRACES[spec['trace']][1].read_text())
    for position, arm in enumerate(spec['order'], 1):
        base = ROOT / 'results/measure' / f"{spec['trace']}-p{spec['pair']}-{arm}"
        launch = json.loads((base / 'launch.json').read_text())
        row = {'trace': spec['trace'], 'pair': spec['pair'], 'arm': arm, 'position': position, 'returncode': launch['returncode'],
               'host_load1_before': launch['host_before']['load1'], 'host_available_gib_before': round(launch['host_before']['available_gib'], 1)}
        result_file = base / 'artifacts/measurement/result.json'
        if result_file.exists():
            r = json.loads(result_file.read_text())
            events = [json.loads(line) for line in (base / 'artifacts/replay/events.jsonl').read_text().splitlines()]
            check = fidelity.compare(recorded, fidelity.load(base / 'artifacts/replay'))
            row.update({'collector_ok': r['ok'], 'collector_failures': r['failures'], 'wall_s': r['wall_ms'] / 1000,
                        'tree_cpu_s': r['tree_cpu_ms'] / 1000, 'agent_cpu_s': r['agent_cpu_ms_last_sample'] / 1000,
                        'agent_cpu_last_sample_before_exit_ms': r['agent_last_sample_before_exit_ms'],
                        'agent_peak_pss_mib': r['agent_peak_pss_mib'], 'tree_peak_pss_mib': r['peak_tree_pss_mib'],
                        'children_peak_pss_mib': r['children_peak_pss_mib'],
                        'non_fixture_wall_s': r['wall_ms'] / 1000 - sum(e['sent_s'] - e['received_s'] for e in events),
                        'observer_cpu_percent_of_wall': 100 * r['observer_cpu_ms'] / r['wall_ms'],
                        'original_cpu_gate_passed': r['original_cpu_gate_passed'], 'cpu_gap_us': r['cpu_gap_us'],
                        'resolution_bound_us': r['resolution_bound_us'], 'max_sample_gap_ms': r['max_sample_gap_ms'],
                        'requests_served': len(events), 'requests_recorded': len(recorded), 'all_requests_ok': all(e['ok'] for e in events),
                        'final_files_equal_recorded_delivery': launch['final_manifest'] == delivery,
                        'fidelity_volatile_classes': check['classes'],
                        'fidelity_residual_messages': [[x.get('first_request'), x.get('message')] for x in check['residual']]})
        rows.append(row)
summary = {}
for trace in TRACES:
    block = {}
    for arm in ('standard-pi', 'pi-bolt'):
        sel = [r for r in rows if r['trace'] == trace and r['arm'] == arm and 'wall_s' in r]
        block[arm] = {m: {'median': statistics.median(r[m] for r in sel), 'min': min(r[m] for r in sel), 'max': max(r[m] for r in sel)} for m in METRICS}
        block[arm]['n'] = len(sel)
    diffs = {}
    for m in METRICS:
        values = []
        for pair in range(1, 6):
            a = [r for r in rows if r['trace'] == trace and r['pair'] == pair and r['arm'] == 'standard-pi' and m in r]
            b = [r for r in rows if r['trace'] == trace and r['pair'] == pair and r['arm'] == 'pi-bolt' and m in r]
            if a and b:
                values.append(a[0][m] - b[0][m])
        diffs[m] = {'median': statistics.median(values), 'min': min(values), 'max': max(values), 'pairs': len(values),
                    'percent_of_pi_median': 100 * statistics.median(values) / block['standard-pi'][m]['median']}
    block['pi_minus_bolt_paired'] = diffs
    summary[trace] = block
(ROOT / 'results/measure-rows.json').write_text(json.dumps(rows, indent=1) + '\n')
(ROOT / 'results/measure-summary.json').write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps(summary, indent=1))
