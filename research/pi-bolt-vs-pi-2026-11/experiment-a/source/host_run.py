"""Host driver for one offline replay launch in the pilot's container isolation.

Usage: host_run.py <label> <arm> <responses_dir> <prompt_file> <base_dir>
Network none, non-root, read-only root, all capabilities dropped. No relay socket, no credential.
"""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT.parent
PILOT = BENCH / 'subscription-pilot/openrouter-v1'
BUILDS = BENCH / 'container-phase1/builds'
IMAGE = 'sha256:9e87977b867847e186d066f531ef783b006d582a985c341c269446088d90f2c4'
D = ['~/.local/bin/docker', '--host', 'unix:///var/run/docker.sock']
PINS = {BUILDS / 'node': 'bc17c508ffeed0ec622934f9b7fa72f8e78da65350e63c3eceb56fa688aa5e12',
        BUILDS / 'bolt/pi': '30164c0edd4bcadfbe2fbb1613c201e82c640a7b01d70d001a9200b1413910b9',
        BUILDS / 'standard/node_modules/@earendil-works/pi-coding-agent/dist/bundle/cli.js': 'e79626f2dd6f94aa45d30f3fa63cd84319a6eefcd150b353cfaf274366926774'}
SKIP = ('node_modules', '.bench-artifacts', '.bench-bin', '.bench-tmp')


def host_state():
    memory = int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))
    return {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'load1': os.getloadavg()[0], 'available_gib': memory / 1048576}


def manifest(base):
    result = {}
    for p in sorted(base.rglob('*')):
        rel = p.relative_to(base)
        if rel.parts[0] in SKIP or not p.is_file() or p.is_symlink():
            continue
        result[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def main():
    label, arm, responses, prompt, base = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve(), Path(sys.argv[4]).resolve(), Path(sys.argv[5]).resolve()
    for p, digest in PINS.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, str(p)
    out = ROOT / 'results' / label
    out.mkdir(parents=True, exist_ok=False)
    work = ROOT / 'workspaces' / label
    shutil.copytree(base, work)
    shutil.copytree(PILOT / 'inputs/node_modules', work / 'node_modules', symlinks=True)
    (work / '.bench-tmp').mkdir()
    (work / '.bench-tmp/package.json').write_text('{"type":"commonjs"}\n')
    (work / '.bench-bin').mkdir()
    (work / '.bench-bin/npm').symlink_to('/inputs/npm/bin/npm-cli.js')
    (work / '.bench-artifacts').mkdir()
    before = host_state()
    assert before['load1'] < 16 and before['available_gib'] >= 8, before
    args = D + ['run', '--rm', '--pull', 'never', '--name', 'bb-expa-' + label.replace('/', '-'), '--label', 'authorization=BB-ORBI-EXPA-OFFLINE',
                '--network', 'none', '--user', '1000:1000', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges=true', '--read-only',
                '--pids-limit', '256', '--memory', '3g', '--memory-swap', '3g', '--cpuset-cpus', '0,1', '--cpus', '2', '--cpu-shares', '128',
                '--tmpfs', '/tmp:rw,noexec,nosuid,nodev,size=512m,mode=1777', '--shm-size', '128m']
    for src, dst, ro in [(ROOT / 'source', '/xa', True), (PILOT / 'results/coding-pair/pi-bolt/runtime-source', '/source', True), (PILOT / 'inputs', '/inputs', True), (BUILDS, '/builds', True),
                         (responses, '/responses', True), (prompt, '/prompt.txt', True), (work, '/work', False)]:
        args += ['--mount', f'type=bind,src={src},dst={dst}' + (',readonly' if ro else '')]
    args += ['--workdir', '/work', '--entrypoint', '/usr/bin/env', IMAGE, '-i', 'PATH=/builds:/usr/local/bin:/usr/bin:/bin', 'HOME=/tmp/home',
             'TMPDIR=/work/.bench-tmp', 'LANG=C.UTF-8', 'LC_ALL=C.UTF-8', 'TZ=UTC', 'PYTHONDONTWRITEBYTECODE=1', 'python3', '/xa/launch.py', arm, '/prompt.txt']
    start = time.time()
    run = subprocess.run(['timeout', '--kill-after=10s', '1900s', *args], capture_output=True, text=True)
    after = host_state()
    shutil.copytree(work / '.bench-artifacts', out / 'artifacts')
    files = manifest(work)
    delivered = out / 'delivered'
    for rel in files:
        target = delivered / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(work / rel, target)
    (out / 'launch.json').write_text(json.dumps({'label': label, 'arm': arm, 'responses': str(responses), 'prompt': str(prompt), 'base': str(base),
        'returncode': run.returncode, 'stdout': run.stdout[-4000:], 'stderr': run.stderr[-4000:], 'host_before': before, 'host_after': after,
        'driver_seconds': time.time() - start, 'final_manifest': files}, indent=2) + '\n')
    shutil.rmtree(work)
    left = subprocess.run(D + ['ps', '--all', '--filter', 'name=bb-expa-' + label.replace('/', '-'), '--format', '{{.ID}}'], capture_output=True, text=True).stdout.strip()
    assert not left, 'owned container still present'
    print(json.dumps({'label': label, 'returncode': run.returncode, 'seconds': round(time.time() - start, 1)}))


if __name__ == '__main__':
    main()
