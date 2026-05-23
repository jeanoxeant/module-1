import os
import socket
import threading
import json

from common.config import (
    BUFFER_SIZE,
    ENCODING
)

SHARED_FOLDER = (
    "peer/storage/shared"
)


class FileServer:
    """
    Peer file upload server.

    Accepts download requests
    from other peers.
    """

    def __init__(
        self,
        host="0.0.0.0",
        port=5001
    ):

        self.host = host
        self.port = port

        os.makedirs(
            SHARED_FOLDER,
            exist_ok=True
        )

        self.server_socket = (
            socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
        )
        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

    def bind(self):
        """
        Bind the server socket to the configured host and port.
        """

        self.server_socket.bind(
            (
                self.host,
                self.port
            )
        )
        self.server_socket.listen()

    def start(self):
        """
        Start server.
        """

        print(
            f"[FILE SERVER RUNNING] "
            f"{self.host}:"
            f"{self.port}"
        )

        while True:

            conn, addr = (
                self.server_socket.accept()
            )

            print(
                f"[CONNECTED] {addr}"
            )

            thread = (
                threading.Thread(
                    target=self.handle_peer,
                    args=(conn,)
                )
            )

            thread.daemon = True
            thread.start()

    def handle_peer(
        self,
        conn
    ):
        """
        Handle peer request.
        """

        try:

            request = conn.recv(
                BUFFER_SIZE
            )

            if not request:
                return

            message = json.loads(
                request.decode(
                    ENCODING
                )
            )

            request_type = (
                message.get(
                    "type"
                )
            )

            # -----------------
            # DOWNLOAD
            # -----------------
            if request_type == (
                "download"
            ):

                filename = (
                    message.get(
                        "filename"
                    )
                )

                self.send_file(
                    conn,
                    filename
                )

        except Exception as e:

            print(
                "[ERROR]",
                str(e)
            )

        finally:
            conn.close()

    def send_file(
        self,
        conn,
        filename
    ):
        """
        Send requested file.
        """

        filepath = os.path.join(
            SHARED_FOLDER,
            filename
        )

        if not os.path.exists(
            filepath
        ):

            print(
                "[ERROR] File not found:",
                filename
            )

            return

        print(
            f"[SENDING] {filename}"
        )

        with open(
            filepath,
            "rb"
        ) as file:

            while True:

                chunk = file.read(
                    BUFFER_SIZE
                )

                if not chunk:
                    break

                conn.sendall(
                    chunk
                )

        print(
            f"[COMPLETE] "
            f"{filename}"
        )