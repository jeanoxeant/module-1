from threading import Lock


class FileIndex:
    """
    Keeps track of shared files and
    which peers own them.
    """

    def __init__(self):
        # filename -> list of peers
        self.files = {}

        # thread safety
        self.lock = Lock()

    def register_files(
        self,
        peer_id,
        ip,
        port,
        file_list
    ):
        """
        Register files for a peer.
        """

        with self.lock:

            for filename in file_list:

                # Create file entry if missing
                if filename not in self.files:
                    self.files[filename] = []

                # Avoid duplicate registration
                peer_exists = any(
                    peer["peer_id"] == peer_id
                    for peer in self.files[filename]
                )

                if not peer_exists:

                    self.files[filename].append({
                        "peer_id": peer_id,
                        "ip": ip,
                        "port": port
                    })

    def search_file(self, filename):
        """
        Search for a file.

        Returns:
            list of peers
        """

        with self.lock:
            return self.files.get(
                filename,
                []
            )

    def remove_peer_files(
        self,
        peer_id
    ):
        """
        Remove all files owned
        by a disconnected peer.
        """

        with self.lock:

            files_to_delete = []

            for filename in self.files:

                self.files[filename] = [
                    peer
                    for peer in self.files[filename]
                    if peer["peer_id"] != peer_id
                ]

                # remove empty entries
                if not self.files[filename]:
                    files_to_delete.append(
                        filename
                    )

            for filename in files_to_delete:
                del self.files[filename]

    def get_all_files(self):
        """
        Return all indexed files.
        """

        with self.lock:
            return self.files

    def file_exists(self, filename):
        """
        Check whether file exists.
        """

        with self.lock:
            return filename in self.files

    def count_files(self):
        """
        Return total indexed files.
        """

        with self.lock:
            return len(self.files)

    def clear(self):
        """
        Remove all indexed files.
        """

        with self.lock:
            self.files.clear()