import socket
import json

from common.config import (
    TRACKER_HOST,
    TRACKER_PORT,
    BUFFER_SIZE,
    ENCODING
)

from common.protocol import (
    REGISTER,
    SEARCH,
    LIST,
    PING,
)


class TrackerClient:
    """
    Handles communication
    with the tracker server.
    """

    def __init__(
        self,
        host=TRACKER_HOST,
        port=TRACKER_PORT
    ):

        self.host = host
        self.port = port

    def _send_request(self, message):
        """
        Send request to tracker
        and return response.
        """

        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            client_socket.connect(
                (self.host, self.port)
            )

            client_socket.send(
                json.dumps(message)
                .encode(ENCODING)
            )

            response = client_socket.recv(
                BUFFER_SIZE
            )

            return json.loads(
                response.decode(
                    ENCODING
                )
            )

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

        finally:
            client_socket.close()

    def register_files(
        self,
        peer_id,
        ip,
        port,
        files
    ):
        """
        Register peer files
        with tracker.
        """

        message = {
            "type": REGISTER,
            "peer_id": peer_id,
            "ip": ip,
            "port": port,
            "files": files
        }

        return self._send_request(
            message
        )

    def ping(self):
        """
        Ping the tracker to verify connectivity.
        """

        return self._send_request({
            "type": PING
        })

    def search_file(
        self,
        filename
    ):
        """
        Search for file
        on tracker.
        """

        message = {
            "type": SEARCH,
            "filename": filename
        }

        return self._send_request(
            message
        )

    def list_files(
        self
    ):
        """
        List all files registered
        with the tracker.
        """

        message = {
            "type": LIST
        }

        return self._send_request(
            message
        )