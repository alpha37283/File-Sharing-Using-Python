import http.server
import socketserver
import json
import os
import socket
import pyqrcode
import webbrowser
import urllib.parse  # For decoding URL paths
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
        super().__init__(*args, directory=build_dir, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/files'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = dict(q.split('=') for q in query.split('&') if '=' in q)
            path = params.get('path', '/')
            
            try:
                files = self.list_files(path)
                self.wfile.write(json.dumps(files).encode())
            except FileNotFoundError as e:
                self.send_error(404, str(e))
        elif self.path.startswith('/download/'):
            file_path = os.path.join(os.getcwd(), urllib.parse.unquote(self.path[10:]))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, 'File not found')
        elif self.path == '/' or not os.path.exists(self.translate_path(self.path)):
            self.path = '/index.html'
            return super().do_GET()
        else:
            return super().do_GET()

    def list_files(self, path):
        # Decode the URL-encoded path (e.g., %2F -> /)
        decoded_path = urllib.parse.unquote(path)

        # Construct the full path
        full_path = os.path.join(os.getcwd(), decoded_path.lstrip('/'))
        print(f"Decoded Path: {decoded_path}, Full Path: {full_path}")  # Debugging log

        # Check if the directory exists
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            raise FileNotFoundError(f"Directory not found: {full_path}")

        # List files and directories
        files = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            files.append({
                'name': item,
                'isDirectory': is_dir,
                'size': os.path.getsize(item_path) if not is_dir else None,
                'lastModified': os.path.getmtime(item_path)
            })
        return files

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def generate_qr_code(link, output_file="myqr.png"):
    qr = pyqrcode.create(link)
    qr.png(output_file, scale=8)
    return output_file

def start_server(directory, port=8010):
    os.chdir(directory)
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        print(f"Access the shared files via: http://{get_local_ip()}:{port}")
        httpd.serve_forever()

class FileSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sharing App")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="Select a folder to share", font=("Arial", 14))
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Folder", command=self.select_folder, font=("Arial", 12))
        self.select_button.pack(pady=10)

        self.qr_label = tk.Label(root, text="", font=("Arial", 10))
        self.qr_label.pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            port = 8010
            ip = get_local_ip()
            link = f"http://{ip}:{port}"

            qr_file = generate_qr_code(link)
            webbrowser.open(qr_file)

            self.qr_label.config(text=f"Sharing at: {link}\nScan the QR Code opened in your browser.")

            server_thread = Thread(target=start_server, args=(folder, port), daemon=True)
            server_thread.start()
        else:
            messagebox.showerror("Error", "No folder selected!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSharingApp(root)
    root.mainloop()
