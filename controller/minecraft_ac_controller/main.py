from http.server import HTTPServer
from .minecraft_communicator import MinecraftHTTPHandler


def run(server_class=HTTPServer, handler_class=MinecraftHTTPHandler, port=8080):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()
