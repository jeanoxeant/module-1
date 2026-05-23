import os
import socket
import json

from common.config import (
    BUFFER_SIZE,
    ENCODING
)

DOWNLOAD_FOLDER = (
    "peer/storage/downloads"
)


class PeerClient:
    """
    Handles direct communication
    with another peer.
    """

    def __init__(self):

        os.makedirs(
            DOWNLOAD_FOLDER,
            exist_ok=True
        )

    def download_file(
        self,
        peer_ip,
        peer_port,
        filename
    ):
        """
        Download a file
        from another peer.
        """

        peer_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            peer_socket.connect(
                (
                    peer_ip,
                    peer_port
                )
            )

            # Request file
            request = {
                "type": "download",
                "filename": filename
            }

            peer_socket.send(
                json.dumps(request)
                .encode(ENCODING)
            )

            save_path = os.path.join(
                DOWNLOAD_FOLDER,
                filename
            )

            with open(
                save_path,
                "wb"
            ) as file:

                while True:

                    data = (
                        peer_socket.recv(
                            BUFFER_SIZE
                        )
                    )

                    if not data:
                        break

                    file.write(data)

            return {
                "status": "success",
                "message":
                    f"{filename} downloaded",
                "path": save_path
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

        finally:
            peer_socket.close()