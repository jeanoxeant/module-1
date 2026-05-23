import socket
import threading
import json
import os

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 9000

PEER_HOST = "10.0.0.17"
PEER_PORT = 5001

SHARED_FOLDER = "shared"

# -----------------------------
# FILE SERVER
# -----------------------------

def handle_download(conn):
    try:
        data = conn.recv(4096)

        message = json.loads(data.decode())

        filename = message["filename"]

        filepath = os.path.join(SHARED_FOLDER, filename)

        if not os.path.exists(filepath):
            conn.close()
            return

        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                conn.sendall(chunk)

    except Exception as e:
        print(e)

    finally:
        conn.close()

def start_file_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((PEER_HOST, PEER_PORT))

    server.listen()

    print(f"[PEER SERVER] {PEER_HOST}:{PEER_PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_download,
            args=(conn,)
        )

        thread.start()

# -----------------------------
# REGISTER FILES
# -----------------------------

def register_files():
    files = os.listdir(SHARED_FOLDER)

    message = {
        "type": "register",
        "ip": PEER_HOST,
        "port": PEER_PORT,
        "files": files
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((TRACKER_HOST, TRACKER_PORT))

    sock.send(json.dumps(message).encode())

    response = sock.recv(4096)

    print(response.decode())

    sock.close()

# -----------------------------
# SEARCH FILE
# -----------------------------

def search_file(filename):
    message = {
        "type": "search",
        "filename": filename
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((TRACKER_HOST, TRACKER_PORT))

    sock.send(json.dumps(message).encode())

    response = json.loads(
        sock.recv(4096).decode()
    )

    sock.close()

    return response["results"]

# -----------------------------
# DOWNLOAD FILE
# -----------------------------

def download_file(peer_ip, peer_port, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((peer_ip, peer_port))

    request = {
        "filename": filename
    }

    sock.send(json.dumps(request).encode())

    with open(f"downloaded_{filename}", "wb") as f:
        while True:
            data = sock.recv(4096)

            if not data:
                break

            f.write(data)

    sock.close()

    print("[DOWNLOAD COMPLETE]")

# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    # Start peer server
    thread = threading.Thread(
        target=start_file_server,
        daemon=True
    )

    thread.start()

    # Register shared files
    register_files()

    while True:
        cmd = input(
            "\n1. Search File\n2. Exit\nChoose: "
        )

        if cmd == "1":
            filename = input("Filename: ")

            results = search_file(filename)

            print(results)

            if results:
                peer_ip, peer_port = results[0]

                download_file(
                    peer_ip,
                    peer_port,
                    filename
                )

        elif cmd == "2":
            break