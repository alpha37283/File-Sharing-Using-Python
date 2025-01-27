import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from utils import get_local_ip, generate_qr_code
from server import start_server
import webbrowser

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
