"""Replay fidelity: compare replayed requests with the recording and across executables.

Volatile classes masked before comparison (durations, timestamps, PIDs, temporary paths); anything left is listed.
Usage: fidelity.py <recorded_relay_dir> <recorded_delivery_manifest> <replay_result_dir>... -> JSON on stdout
"""
import json
import re
import sys
from pathlib import Path

MASKS = [
    ('temp_path', re.compile(r'pi-bash-[0-9a-f]{16}\.log')),
    ('timestamp', re.compile(r'\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?')),
    ('timestamp', re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+(\d{2}:\d{2}|\d{4})')),
    ('timestamp', re.compile(r'\b\d{2}:\d{2}:\d{2}\b')),
    ('duration', re.compile(r'\b\d+(\.\d+)?\s?(ms|s|m)\b')),
    ('pid', re.compile(r'\b(pid|PID)[ =:]+\d+')),
]


def mask(text):
    used = set()
    for name, pattern in MASKS:
        text, n = pattern.subn(f'<{name}>', text)
        if n:
            used.add(name)
    return text, used


def content(message):
    c = message.get('content')
    if isinstance(c, list):
        return '\n'.join(p.get('text', '') for p in c)
    return c or ''


def compare(a_requests, b_requests):
    report = {'count': [len(a_requests), len(b_requests)], 'identical_requests': 0, 'masked_equal_requests': 0,
              'classes': {}, 'residual': []}
    seen = set()
    for i, (a, b) in enumerate(zip(a_requests, b_requests), 1):
        if a == b:
            report['identical_requests'] += 1
            continue
        clean = True
        for key in sorted(set(a) | set(b)):
            if key == 'messages' or a.get(key) == b.get(key):
                continue
            clean = False
            if ('key', key) not in seen:
                seen.add(('key', key))
                report['residual'].append({'request': i, 'field': key})
        ma, mb = a['messages'], b['messages']
        if len(ma) != len(mb):
            clean = False
            report['residual'].append({'request': i, 'field': 'message_count', 'a': len(ma), 'b': len(mb)})
        for n, (x, y) in enumerate(zip(ma, mb)):
            if x == y:
                continue
            tx, used_x = mask(content(x))
            ty, used_y = mask(content(y))
            same_rest = {k: v for k, v in x.items() if k != 'content'} == {k: v for k, v in y.items() if k != 'content'}
            if tx == ty and same_rest:
                for name in used_x | used_y:
                    report['classes'][name] = report['classes'].get(name, 0) + (0 if (n, name) in seen else 1)
                    seen.add((n, name))
                continue
            clean = False
            if ('msg', n) in seen:
                continue
            seen.add(('msg', n))
            la, lb = tx.splitlines(), ty.splitlines()
            lines = [(p, q) for p, q in zip(la, lb) if p != q][:6]
            report['residual'].append({'first_request': i, 'message': n, 'role': x.get('role'), 'line_counts': [len(la), len(lb)],
                                       'differing_lines': lines})
        if clean:
            report['masked_equal_requests'] += 1
    return report


def load(directory):
    return [json.loads(p.read_text()) for p in sorted(Path(directory).glob('*-request.json'))]


if __name__ == '__main__':
    recorded = load(sys.argv[1])
    delivery = json.loads(Path(sys.argv[2]).read_text())
    runs = {Path(p).name: Path(p) for p in sys.argv[3:]}
    replays = {name: load(path / 'artifacts/replay') for name, path in runs.items()}
    manifests = {name: json.loads((path / 'launch.json').read_text())['final_manifest'] for name, path in runs.items()}
    out = {'vs_recording': {name: compare(recorded, reqs) for name, reqs in replays.items()}}
    names = list(runs)
    out['cross_executable'] = compare(replays[names[0]], replays[names[1]])
    out['final_files'] = {name: {'equal_to_recorded_delivery': m == delivery,
                                 'differing': sorted(k for k in set(m) | set(delivery) if m.get(k) != delivery.get(k))} for name, m in manifests.items()}
    out['final_files_equal_across_executables'] = manifests[names[0]] == manifests[names[1]]
    print(json.dumps(out, indent=1))
