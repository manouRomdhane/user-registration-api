from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/send":
            length = int(self.headers.get('Content-Length', '0'))
            payload = self.rfile.read(length).decode('utf-8')
            try:
                data = json.loads(payload)
            except Exception:
                data = {"raw": payload}

            print(f"[EMAIL-MOCK] Sending activation code to: {data.get('email', '<redacted>')}")

            self.send_response(202)
            self.end_headers()
            self.wfile.write(b'{"status":"accepted"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 3001), Handler)
    print("[EMAIL-MOCK] Running on :3001")
    server.serve_forever()
