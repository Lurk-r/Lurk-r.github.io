#!/usr/bin/env python3
"""
PixelGun Ban Checker - Local Proxy Server
Bypasses CORS restrictions for browser-based API calls
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
import ssl

class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/proxy':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body)

                method = data.get('method', 'GET')
                url = data.get('url', '')
                request_headers = data.get('headers', {})
                request_body = data.get('body', '')

                # Create SSL context that doesn't verify certificates (for simplicity)
                # In production, you should use proper certificate verification
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                # Build request
                req = urllib.request.Request(url, method=method)

                # Add headers
                for key, value in request_headers.items():
                    req.add_header(key, value)

                # Add body if present
                if request_body:
                    if isinstance(request_body, str):
                        request_body = request_body.encode('utf-8')
                    req.data = request_body

                # Make the request
                try:
                    with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
                        response_body = response.read().decode('utf-8')
                        response_status = response.status
                except urllib.error.HTTPError as e:
                    response_body = e.read().decode('utf-8')
                    response_status = e.code

                # Send response
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                result = {
                    'success': True,
                    'status': response_status,
                    'body': response_body
                }
                self.wfile.write(json.dumps(result).encode('utf-8'))

            except Exception as e:
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                result = {
                    'success': False,
                    'error': str(e)
                }
                self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=9999):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"🚀 Proxy server running on http://localhost:{port}")
    print(f"✅ Open index.html in your browser to use the Ban Checker")
    print(f"🛑 Press Ctrl+C to stop")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()