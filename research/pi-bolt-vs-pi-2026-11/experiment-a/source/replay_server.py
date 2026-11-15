"""Offline replay fixture: serves saved model responses in order on container loopback.

No upstream connection, credential or retry exists here. Request N receives saved
response N byte for byte; a request beyond the recording gets HTTP 500.
"""
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

responses = [p.read_bytes() for p in sorted(Path(sys.argv[1]).glob('*-response.sse'))]
out = Path(sys.argv[2])
out.mkdir(parents=True)
count = 0


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *args):
        pass

    def do_POST(self):
        global count
        self.close_connection = True
        raw = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        received = time.perf_counter()
        index = count
        count += 1
        (out / f'{index+1:04d}-request.json').write_bytes(raw)
        ok = self.path == '/api/v1/chat/completions' and index < len(responses)
        body = responses[index] if ok else json.dumps({'error': {'message': 'beyond_recording'}}).encode()
        self.send_response(200 if ok else 500)
        self.send_header('Content-Type', 'text/event-stream' if ok else 'application/json')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()
        with (out / 'events.jsonl').open('a') as log:
            log.write(json.dumps({'request': index+1, 'ok': ok, 'path': self.path, 'request_bytes': len(raw),
                                  'response_bytes': len(body), 'received_s': received,
                                  'sent_s': time.perf_counter()}) + '\n')


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8765), Handler)
    (out / 'ready').write_text(str(len(responses)))
    server.serve_forever(poll_interval=0.2)
