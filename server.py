import os
import socketserver
from request_handler import CustomHTTPRequestHandler
from utils import get_local_ip

def start_server(directory, port=8010):
    os.chdir(directory)
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        print(f"Access the shared files via: http://{get_local_ip()}:{port}")
        httpd.serve_forever()
