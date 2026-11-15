"""In-container launcher: start the replay fixture, then one agent under the collector.

Same agent configuration as the pilot's coding_run.py; the only provider endpoint is the
loopback fixture and the key is a dummy string.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

arm, prompt_file = sys.argv[1], sys.argv[2]
MODEL = 'deepseek/deepseek-v4.1-flash-1017'
ROUTING = {'only': ['deepinfra/fp8'], 'order': ['deepinfra/fp8'], 'allow_fallbacks': False, 'require_parameters': True,
           'data_collection': 'deny', 'max_price': {'prompt': 0.3, 'completion': 1.2, 'request': 0, 'image': 0, 'audio': 0}}
commands = {'standard-pi': ['/builds/node', '/builds/standard/node_modules/@earendil-works/pi-coding-agent/dist/bundle/cli.js'],
            'pi-bolt': ['/builds/bolt/pi']}
home = Path('/tmp/home')
agent = home / 'agent'
agent.mkdir(parents=True)
(agent / 'auth.json').write_text(json.dumps({'openrouter': {'type': 'api_key', 'key': 'benchmark-local-replay-not-a-real-key'}}))
(agent / 'models.json').write_text(json.dumps({'providers': {'openrouter': {'baseUrl': 'http://127.0.0.1:8765/api/v1', 'modelOverrides': {MODEL: {'maxTokens': 65536, 'compat': {'openRouterRouting': ROUTING, 'supportsStore': False, 'maxTokensField': 'max_tokens'}}}}}}))
(agent / 'settings.json').write_text(json.dumps({'cacheWarming': 'off', 'retry': {'enabled': False, 'provider': {'maxRetries': 0}}, 'compaction': {'enabled': False}}))
common = ['--mode', 'json', '--no-session', '--offline', '--no-approve', '--no-extensions', '--no-mcp', '--no-themes', '--no-skills',
          '--no-prompt-templates', '--no-context-files', '--tools', 'read,bash,edit,write', '--provider', 'openrouter', '--model', MODEL,
          '--thinking', 'high', '--system-prompt', Path('/inputs/system-prompt.txt').read_text(), '-p', Path(prompt_file).read_text()]
env = {'PATH': '/work/.bench-bin:/builds:/usr/local/bin:/usr/bin:/bin', 'HOME': str(home), 'TMPDIR': '/work/.bench-tmp',
       'PI_CODING_AGENT_DIR': str(agent), 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TZ': 'UTC', 'PYTHONDONTWRITEBYTECODE': '1'}
out = Path('/work/.bench-artifacts')
# The fixture writes outside /work so the agent's own find/grep sees the same workspace layout as the recording.
replay = Path('/tmp/replay')
server = subprocess.Popen([sys.executable, '/xa/replay_server.py', '/responses', str(replay)])
try:
    deadline = time.monotonic() + 10
    while not (replay / 'ready').exists():
        assert time.monotonic() < deadline and server.poll() is None, 'fixture did not start'
        time.sleep(0.05)
    time.sleep(0.3)
    config = {'argv': commands[arm] + common, 'cwd': '/work', 'env': env, 'out': str(out / 'measurement'),
              'sample_interval_s': .25, 'sample_memory': True, 'timeout_s': 1800}
    path = out / 'accounting-config.json'
    path.write_text(json.dumps(config, indent=2) + '\n')
    run = subprocess.run([sys.executable, '/xa/accounting.py', str(path)], timeout=1830, stdout=subprocess.DEVNULL)
finally:
    server.terminate()
    server.wait(10)
    import shutil
    shutil.copytree(replay, out / 'replay')
raise SystemExit(run.returncode)
