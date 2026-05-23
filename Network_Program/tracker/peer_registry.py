from threading import Lock


class PeerRegistry:
    """
    Stores and manages connected peers.
    """

    def __init__(self):
        self.peers = {}

        # Prevent race conditions
        self.lock = Lock()

    def register_peer(
        self,
        peer_id,
        ip,
        port
    ):
        """
        Register a peer or update it if it already exists.
        """

        with self.lock:
            self.peers[peer_id] = {
                "peer_id": peer_id,
                "ip": ip,
                "port": port
            }

    def peer_exists(self, peer_id):
        """
        Check if peer exists.
        """

        with self.lock:
            return peer_id in self.peers

    def get_peer(self, peer_id):
        """
        Return peer information.
        """

        with self.lock:
            return self.peers.get(peer_id)

    def get_all_peers(self):
        """
        Return all connected peers.
        """

        with self.lock:
            return list(self.peers.values())

    def remove_peer(self, peer_id):
        """
        Remove peer from registry.
        """

        with self.lock:
            if peer_id in self.peers:
                del self.peers[peer_id]

    def update_peer(
        self,
        peer_id,
        ip=None,
        port=None
    ):
        """
        Update peer info.
        """

        with self.lock:

            if peer_id not in self.peers:
                return False

            if ip:
                self.peers[peer_id]["ip"] = ip

            if port:
                self.peers[peer_id]["port"] = port

            return True

    def count_peers(self):
        """
        Return total number of peers.
        """

        with self.lock:
            return len(self.peers)

    def clear(self):
        """
        Remove all peers.
        """

        with self.lock:
            self.peers.clear()