import threading

from peer.network.file_server import (
    FileServer
)

from peer.gui.app import App

from common.config import (
    DEFAULT_PEER_HOST,
    DEFAULT_PEER_PORT
)


def start_file_server(start_port=DEFAULT_PEER_PORT):
    """
    Start peer file server, trying the default port first and
    falling back to the next available port if necessary.
    """

    port = start_port
    while True:
        server = FileServer(
            host=DEFAULT_PEER_HOST,
            port=port
        )
        try:
            server.bind()
            break
        except OSError as e:
            print(f"[FILE SERVER] Port {port} unavailable: {e}")
            port += 1
            if port > start_port + 20:
                raise

    thread = threading.Thread(
        target=server.start,
        daemon=True
    )
    thread.start()
    return port


def main():
    """
    Application entry point.
    """

    # Start file server thread and use the bound port in the GUI
    peer_port = start_file_server()

    # Launch GUI
    app = App(peer_port=peer_port)
    app.run()


if __name__ == "__main__":
    main()