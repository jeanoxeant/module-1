# P2P File Sharing Application

## Overview

This project is a Peer-to-Peer (P2P) file-sharing application built using Python. The application allows peers to communicate directly and transfer files over a network using TCP sockets.

A tracker server is used to help peers discover one another, but actual file transfers occur directly between peers.

This project demonstrates networking concepts including:

- Peer-to-peer communication
- TCP socket programming
- Request/response communication
- Multi-threading
- JSON-based messaging
- File transfer between computers

---

## Networking Model

This project uses the **Peer-to-Peer (P2P)** networking model.

In a peer-to-peer system, computers communicate directly with each other instead of routing all communication through a central server.

The tracker server is only responsible for:

- Registering peers
- Registering shared files
- Searching for file locations

Actual file transfers happen directly between peers.

### Architecture

```text
                +------------------+
                |  Tracker Server  |
                +------------------+
                       ^
                       |
        -----------------------------------
        |                                 |
        |                                 |
    +--------+                       +--------+
    | Peer A |<-------------------->| Peer B |
    +--------+      File Transfer   +--------+