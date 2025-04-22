from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from process_biome import process_biome

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Read the data
        try:
            data = json.loads(post_data)
            process_biome(data)
            self.send_response(200)
        except json.JSONDecodeError:
            self.send_response(400)

        self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()
