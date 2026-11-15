"""Run the fixed measurement schedule sequentially. No retries; a failed launch is kept and the run continues."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PILOT = ROOT.parent / 'subscription-pilot/openrouter-v1'
TRACES = {'pitrace': PILOT / 'results/coding-pair/relay', 'bolttrace': PILOT / 'results/coding-pair/pi-bolt/relay'}
for spec in json.loads((ROOT / 'schedule.json').read_text())['pairs']:
    for arm in spec['order']:
        label = f"measure/{spec['trace']}-p{spec['pair']}-{arm}"
        run = subprocess.run([sys.executable, str(ROOT / 'source/host_run.py'), label, arm, str(TRACES[spec['trace']]),
                              str(PILOT / 'inputs/task-prompt.txt'), str(PILOT / 'inputs/base')], capture_output=True, text=True)
        print(label, run.returncode, run.stdout.strip()[-120:], run.stderr.strip()[-300:], flush=True)
