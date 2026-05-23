import sys
import socket
import threading
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from common.protocol import (
    LIST,
    PING,
    create_success_response,
    create_error_response,
)

HOST = "0.0.0.0"
PORT = 9000

# filename -> [(ip, port)]
shared_files = {}

# connected peers
peers = []

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    try:
        while True:
            data = conn.recv(4096)

            if not data:
                break

            message = json.loads(data.decode())

            message_type = message["type"]

            # REGISTER FILES
            if message_type == "register":
                peer_ip = message["ip"]
                peer_port = message["port"]

                for filename in message["files"]:
                    if filename not in shared_files:
                        shared_files[filename] = []

                    shared_files[filename].append(
                        (peer_ip, peer_port)
                    )

                print(shared_files)

                conn.send(
                    json.dumps(create_success_response(
                        message="ok"
                    )).encode()
                )

            # SEARCH FILE
            elif message_type == "search":
                filename = message["filename"]

                results = shared_files.get(filename, [])

                conn.send(
                    json.dumps(create_success_response(
                        data={
                            "results": results
                        }
                    )).encode()
                )

            # LIST ALL FILES
            elif message_type == LIST:
                conn.send(
                    json.dumps(create_success_response(
                        data={
                            "results": shared_files
                        }
                    )).encode()
                )

            # PING
            elif message_type == PING:
                conn.send(
                    json.dumps(create_success_response(
                        message="pong"
                    )).encode()
                )

    except Exception as e:
        print(e)

    finally:
        conn.close()

def start_tracker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen()

    print(f"[TRACKER RUNNING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )

        thread.start()

if __name__ == "__main__":
    start_tracker()