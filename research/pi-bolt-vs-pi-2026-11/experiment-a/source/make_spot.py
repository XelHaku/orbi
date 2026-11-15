"""Build the parity spot-check fixture: scripted responses in the recorded stream format, plus a small workspace."""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
(out / 'responses').mkdir(parents=True)
(out / 'base/spot').mkdir(parents=True)
(out / 'base/spot/a.txt').write_bytes('alpha\nbeta unique-marker\ngamma\nrepeat\nrepeat\n'.encode())
(out / 'base/spot/crlf.txt').write_bytes('uno\r\ndos\r\ntres é中\r\ncuatro\r\n'.encode())
(out / 'prompt.txt').write_text('Parity spot check. Follow the scripted tool calls exactly.\n')

HEAD = {'id': 'gen-spot', 'object': 'chat.completion.chunk', 'created': 1, 'model': 'deepseek/deepseek-v4.1-flash-1017', 'provider': 'DeepInfra'}


def chunk(delta, finish=None, native=None, usage=None):
    body = {**HEAD, 'choices': [{'index': 0, 'delta': delta, 'finish_reason': finish, 'native_finish_reason': native}]}
    if usage:
        body['usage'] = usage
    return 'data: ' + json.dumps(body, separators=(',', ':'), ensure_ascii=False) + '\n\n'


USAGE = {'prompt_tokens': 10, 'completion_tokens': 10, 'total_tokens': 20, 'cost': 0}


def calls(items, native='tool_calls', split=None):
    text = ''
    for i, (name, args) in enumerate(items):
        text += chunk({'content': None, 'role': 'assistant', 'tool_calls': [{'index': i, 'id': f'call-spot-{i}', 'type': 'function', 'function': {'name': name, 'arguments': ''}}]})
        raw = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
        pieces = [raw[:split], raw[split:]] if split else [raw]
        for piece in pieces:
            text += chunk({'content': None, 'role': 'assistant', 'tool_calls': [{'index': i, 'function': {'arguments': piece}}]})
    text += chunk({'content': '', 'role': 'assistant'}, 'tool_calls', native)
    text += chunk({'content': '', 'role': 'assistant'}, 'tool_calls', native, USAGE)
    return text + 'data: [DONE]\n\n'


steps = [
    calls([('bash', {'command': "printf 'out-line\\n'; printf 'err-line\\n' >&2; exit 3", 'timeout': 20})]),
    calls([('write', {'path': 'spot/new.txt', 'content': 'línea uno\r\nline two 中文\n'})], split=31),
    calls([('edit', {'path': 'spot/a.txt', 'edits': [{'oldText': 'beta unique-marker', 'newText': 'beta EDITED'}]})]),
    calls([('edit', {'path': 'spot/a.txt', 'edits': [{'oldText': 'not-present-anywhere', 'newText': 'x'}]})]),
    calls([('edit', {'path': 'spot/a.txt', 'edits': [{'oldText': 'repeat', 'newText': 'once'}]})]),
    calls([('read', {'path': 'spot/crlf.txt', 'offset': 2, 'limit': 2}), ('read', {'path': 'spot/missing.txt', 'offset': None, 'limit': None})]),
    calls([('bash', {'command': 'seq 1 20000', 'timeout': 20})]),
    calls([('bash', '{}')], native='length'),
    calls([('bash', {'command': 'sleep 5', 'timeout': 1})]),
    calls([('bash', {'command': 'cat spot/new.txt spot/a.txt | sha256sum', 'timeout': 20})]),
    chunk({'content': 'Spot check complete.', 'role': 'assistant'}) + chunk({'content': '', 'role': 'assistant'}, 'stop', 'stop')
    + chunk({'content': '', 'role': 'assistant'}, 'stop', 'stop', USAGE) + 'data: [DONE]\n\n',
]
for i, text in enumerate(steps, 1):
    (out / f'responses/{i:04d}-response.sse').write_bytes(text.encode())
print(len(steps))
