import http.server
import json
import ssl
import socketserver
import sys


class MockJSONbinHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            record = json.loads(body) if body else {}
        except Exception:
            record = {}
        bin_id = "mock-bin-id-001"
        response = {
            "record": record,
            "metadata": {
                "id": bin_id,
                "createdAt": "2024-01-01T00:00:00.000Z",
                "private": True
            }
        }
        data = json.dumps(response).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        bin_id = self.path.rstrip('/').split('/')[-1].split('?')[0]
        response = {
            "record": {"test": "hello"},
            "metadata": {
                "id": bin_id,
                "createdAt": "2024-01-01T00:00:00.000Z",
                "private": True
            }
        }
        data = json.dumps(response).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_PUT(self):
        bin_id = self.path.rstrip('/').split('/')[-1]
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            record = json.loads(body) if body else {}
        except Exception:
            record = {}
        response = {
            "record": record,
            "metadata": {
                "parentId": bin_id,
                "id": bin_id + "-v2",
                "createdAt": "2024-01-01T00:00:00.000Z"
            }
        }
        data = json.dumps(response).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_DELETE(self):
        bin_id = self.path.rstrip('/').split('/')[-1]
        response = {
            "message": "Bin deleted successfully",
            "metadata": {
                "id": bin_id
            }
        }
        data = json.dumps(response).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 443
use_ssl = sys.argv[2] == "ssl" if len(sys.argv) > 2 else True

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('0.0.0.0', port), MockJSONbinHandler)

if use_ssl:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/tmp/mock-cert.pem', '/tmp/mock-key.pem')
    # Allow all TLS versions for compatibility
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

httpd.serve_forever()
