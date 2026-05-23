import customtkinter as ctk
from tkinter import filedialog
import shutil
import socket
import uuid
import os

from common.config import (
    DEFAULT_PEER_PORT,
    TRACKER_HOST,
    TRACKER_PORT,
    SHARED_FOLDER,
)
from common.constants import (
    DEFAULT_PEER_ID,
)
from peer.network.tracker_client import TrackerClient
from peer.network.peer_client import PeerClient
from peer.network.upload import upload_file as upload_file_to_shared_folder


class App:
    def __init__(self, peer_port=DEFAULT_PEER_PORT):
        ctk.set_appearance_mode("gray")
        ctk.set_default_color_theme("blue")

        self.peer_id = f"{DEFAULT_PEER_ID}-{uuid.uuid4().hex[:8]}"
        self.peer_host = self._detect_peer_host()
        self.peer_port = peer_port
        self.tracker_host = TRACKER_HOST
        self.tracker_port = TRACKER_PORT
        self.tracker_client = TrackerClient(
            host=self.tracker_host,
            port=self.tracker_port
        )
        self.peer_client = PeerClient()
        self.search_results = []

        self.app = ctk.CTk()
        self.app.title("Jean Oxeant - P2P File Sharing")
        self.app.geometry("900x600")

        self._create_header()
        self._create_status()
        self._create_tracker_frame()
        self._create_shared_files_frame()
        self._create_search_frame()
        self._create_results_frame()
        self._create_buttons()

        self._load_shared_files()
        self._check_tracker_connection()
        self.register_shared_files()

    def _detect_peer_host(self):
        try:
            host = socket.gethostbyname(socket.gethostname())
            if host.startswith("127."):
                host = "127.0.0.1"
        except Exception:
            host = "127.0.0.1"
        return host

    def _create_header(self):
        title = ctk.CTkLabel(
            self.app,
            text="Jean Oxeant - P2P File Sharing",
            font=("Arial", 28)
        )
        title.pack(pady=20)

    def _create_status(self):
        self.status_label = ctk.CTkLabel(
            self.app,
            text="Tracker: Connecting..."
        )
        self.status_label.pack(pady=5)

    def _create_tracker_frame(self):
        tracker_frame = ctk.CTkFrame(self.app)
        tracker_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tracker_host_label = ctk.CTkLabel(
            tracker_frame,
            text="Tracker Host:"
        )
        tracker_host_label.pack(
            side="left",
            padx=(0, 5),
            pady=10
        )

        self.tracker_host_entry = ctk.CTkEntry(
            tracker_frame,
            width=180
        )
        self.tracker_host_entry.insert(0, self.tracker_host)
        self.tracker_host_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        tracker_port_label = ctk.CTkLabel(
            tracker_frame,
            text="Port:"
        )
        tracker_port_label.pack(
            side="left",
            padx=(10, 5),
            pady=10
        )

        self.tracker_port_entry = ctk.CTkEntry(
            tracker_frame,
            width=80
        )
        self.tracker_port_entry.insert(0, str(self.tracker_port))
        self.tracker_port_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        set_tracker_button = ctk.CTkButton(
            tracker_frame,
            text="Set Tracker",
            command=self.set_tracker_address
        )
        set_tracker_button.pack(
            side="left",
            padx=10,
            pady=10
        )

    def _create_shared_files_frame(self):
        shared_frame = ctk.CTkFrame(self.app)
        shared_frame.pack(
            fill="both",
            padx=20,
            pady=10
        )

        shared_label = ctk.CTkLabel(
            shared_frame,
            text="Shared Files",
            font=("Arial", 20)
        )
        shared_label.pack(pady=10)

        self.shared_listbox = ctk.CTkTextbox(
            shared_frame,
            height=120
        )
        self.shared_listbox.pack(
            fill="both",
            padx=10,
            pady=10
        )

        shared_buttons = ctk.CTkFrame(shared_frame)
        shared_buttons.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        upload_button = ctk.CTkButton(
            shared_buttons,
            text="Upload File",
            command=self.upload_file
        )
        upload_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        refresh_button = ctk.CTkButton(
            shared_buttons,
            text="Refresh Shared Files",
            command=self._load_shared_files
        )
        refresh_button.pack(
            side="left",
            padx=5,
            pady=5
        )

    def _create_search_frame(self):
        search_frame = ctk.CTkFrame(self.app)
        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter filename..."
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_files
        )
        self.search_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.browse_button = ctk.CTkButton(
            search_frame,
            text="Browse Remote Files",
            command=self.browse_remote_files
        )
        self.browse_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.download_button = ctk.CTkButton(
            search_frame,
            text="Download First Result",
            command=self.download_selected_file
        )
        self.download_button.pack(
            side="left",
            padx=10,
            pady=10
        )

    def _create_results_frame(self):
        results_frame = ctk.CTkFrame(self.app)
        results_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        results_label = ctk.CTkLabel(
            results_frame,
            text="Search Results",
            font=("Arial", 20)
        )
        results_label.pack(pady=10)

        self.results_box = ctk.CTkTextbox(results_frame)
        self.results_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def _create_buttons(self):
        buttons_frame = ctk.CTkFrame(self.app)
        buttons_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        upload_button = ctk.CTkButton(
            buttons_frame,
            text="Upload File",
            command=self.upload_file
        )
        upload_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="Refresh Shared Files",
            command=self._load_shared_files
        )
        refresh_button.pack(
            side="left",
            padx=10,
            pady=10
        )

    def _load_shared_files(self):
        os.makedirs(SHARED_FOLDER, exist_ok=True)
        self.shared_listbox.delete("1.0", "end")
        for filename in sorted(os.listdir(SHARED_FOLDER)):
            filepath = os.path.join(SHARED_FOLDER, filename)
            if os.path.isfile(filepath):
                self.shared_listbox.insert("end", f"{filename}\n")

    def _check_tracker_connection(self):
        response = self.tracker_client.ping()
        if response.get("status") == "error":
            self.update_status("Tracker unavailable")
            return False

        self.update_status(
            f"Connected to {self.tracker_host}:{self.tracker_port}"
        )
        return True

    def set_tracker_address(self):
        host = self.tracker_host_entry.get().strip()
        port_text = self.tracker_port_entry.get().strip()

        if not host:
            self.update_status("Tracker host cannot be empty")
            return

        try:
            port = int(port_text)
        except ValueError:
            self.update_status("Tracker port must be a number")
            return

        self.tracker_host = host
        self.tracker_port = port
        self.tracker_client = TrackerClient(
            host=self.tracker_host,
            port=self.tracker_port
        )

        if self._check_tracker_connection():
            self.update_status(
                f"Using tracker {self.tracker_host}:{self.tracker_port}"
            )
        else:
            self.update_status(
                f"Could not connect to {self.tracker_host}:{self.tracker_port}"
            )

    def upload_file(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        try:
            filename, destination = upload_file_to_shared_folder(filepath)
        except Exception as e:
            self.update_status(f"Upload failed: {e}")
            return

        self.shared_listbox.insert("end", f"{filename}\n")
        self.register_shared_files()
        self.update_status(f"Uploaded {filename} and registered with tracker")

    def search_files(self):
        filename = self.search_entry.get().strip()
        if not filename:
            self.update_status("Enter a filename to search")
            return

        response = self.tracker_client.search_file(filename)
        if response.get("status") == "error":
            self.update_status(response.get("message", "Tracker search failed"))
            return

        results = response.get("data", {}).get("results", [])
        self.search_results = results

        self.results_box.delete("1.0", "end")
        if not results:
            self.results_box.insert("end", "No peers have that file.\n")
            self.update_status("No peers found")
            return

        for index, peer in enumerate(results, start=1):
            peer_ip, peer_port = peer
            self.results_box.insert(
                "end",
                f"{index}. {filename} @ {peer_ip}:{peer_port}\n"
            )

        self.update_status(f"Found {len(results)} peer(s)")

    def browse_remote_files(self):
        response = self.tracker_client.list_files()
        if response.get("status") == "error":
            self.update_status(response.get("message", "Tracker list failed"))
            return

        results = response.get("data", {}).get("results", {})

        self.results_box.delete("1.0", "end")
        if not results:
            self.results_box.insert("end", "No remote files available.\n")
            self.update_status("No remote files found")
            return

        for filename, peers in results.items():
            self.results_box.insert("end", f"{filename}\n")
            for peer_ip, peer_port in peers:
                self.results_box.insert(
                    "end",
                    f"  - {peer_ip}:{peer_port}\n"
                )
            self.results_box.insert("end", "\n")

        self.update_status(f"Listed {len(results)} remote file(s)")

    def download_selected_file(self):
        if not self.search_results:
            self.update_status("Search for a file before downloading")
            return

        peer_ip, peer_port = self.search_results[0]
        filename = self.search_entry.get().strip()
        if not filename:
            self.update_status("Enter a filename to download")
            return

        result = self.peer_client.download_file(
            peer_ip,
            peer_port,
            filename
        )

        if result.get("status") == "success":
            self.update_status(result.get("message", "Download complete"))
            self.results_box.insert("end", f"Downloaded to {result.get('path')}\n")
        else:
            self.update_status(result.get("message", "Download failed"))
            self.results_box.insert("end", f"Download failed: {result.get('message')}\n")

    def register_shared_files(self):
        try:
            filenames = [
                f for f in os.listdir(SHARED_FOLDER)
                if os.path.isfile(os.path.join(SHARED_FOLDER, f))
            ]
        except FileNotFoundError:
            filenames = []

        if not filenames:
            self.update_status("No shared files to register")
            return

        response = self.tracker_client.register_files(
            self.peer_id,
            self.peer_host,
            self.peer_port,
            filenames
        )

        if response.get("status") in ("ok", "success"):
            self.update_status("Shared files registered with tracker")
        else:
            self.update_status(response.get("message", "Failed to register files"))

    def update_status(self, message):
        self.status_label.configure(text=f"Tracker: {message}")

    def run(self):
        self.app.mainloop()
