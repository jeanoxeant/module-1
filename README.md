# P2P File Sharing Application

    # Overview

This project is a Peer-to-Peer (P2P) file-sharing application built using Python. The application allows peers to communicate directly and transfer files over a network using TCP sockets.

A tracker server is used to help peers discover one another, but actual file transfers occur directly between peers.

- Peer-to-peer communication
- TCP socket programming
- Request/response communication
- Multi-threading
- JSON-based messaging
- File transfer between computers


My purpose to write this project is to make it easy to transfer my files in my work area with my companions.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (you will need to show two pieces of software running and communicating with each other) and a walkthrough of the code.}

https://youtu.be/WXd67JXlSW8

# Network Communication

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

I used TCP. port 9000 for the tracker, 5001 for the local.

{Identify the format of messages being sent between the client and server or the messages sent between two peers.}

# Development Environment

I used Virtual Studio code to create my application.

I used Python to creates my program and also I used some libraries like, socket, server.

# Useful Websites

* https://docs.python.org/3/library/socketserver.html
* https://docs.python.org/3/library/socket.html

# Future Work

* a conversation chat between users.
* a better gui that can have more options.
* video calling between users.