from http.server import HTTPServer
from .minecraft_communicator import MinecraftHTTPHandler
from .ac_communicator import AirConditioner

def start_ac_handler(ac, server_class=HTTPServer, handler_class=MinecraftHTTPHandler, port=8080):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class, ac)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


def main():
    ac = AirConditioner()
    ac.connect_device()
    start_ac_handler(ac)

if __name__ == "__main__":
    main()


