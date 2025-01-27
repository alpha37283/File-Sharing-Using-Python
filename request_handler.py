import http.server
import os
import urllib.parse
import json

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
        super().__init__(*args, directory=build_dir, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/files'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            query = ''
            if '?' in self.path:
                query = self.path.split('?')[1]

            params = {}
            if query:
                query_parts = query.split('&')
                for q in query_parts:
                    if '=' in q:
                        key, value = q.split('=')
                        params[key] = value

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
        decoded_path = urllib.parse.unquote(path)
        full_path = os.path.join(os.getcwd(), decoded_path.lstrip('/'))
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            raise FileNotFoundError(f"Directory not found: {full_path}")

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
