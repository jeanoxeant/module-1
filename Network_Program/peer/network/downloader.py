import threading

from peer.network.peer_client import PeerClient


class Downloader:
    """
    Handles file downloads.

    Supports threaded downloads so the GUI
    does not freeze.
    """

    def __init__(self):
        self.peer_client = PeerClient()

        # active downloads
        self.active_downloads = {}

    def download_file(
        self,
        peer_ip,
        peer_port,
        filename,
        callback=None
    ):
        """
        Start file download in a thread.

        callback:
            optional function called
            when download completes
        """

        thread = threading.Thread(
            target=self._download_worker,
            args=(
                peer_ip,
                peer_port,
                filename,
                callback
            )
        )

        thread.daemon = True
        thread.start()

        self.active_downloads[
            filename
        ] = thread

    def _download_worker(
        self,
        peer_ip,
        peer_port,
        filename,
        callback=None
    ):
        """
        Background worker for download.
        """

        response = (
            self.peer_client.download_file(
                peer_ip=peer_ip,
                peer_port=peer_port,
                filename=filename
            )
        )

        print(response)

        # remove finished thread
        self.active_downloads.pop(
            filename,
            None
        )

        # notify GUI if callback exists
        if callback:
            callback(response)

    def is_downloading(
        self,
        filename
    ):
        """
        Check if file is downloading.
        """

        return (
            filename
            in self.active_downloads
        )

    def get_active_downloads(self):
        """
        Return active downloads.
        """

        return list(
            self.active_downloads.keys()
        )