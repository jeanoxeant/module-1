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


    ------------------------------------------
    # Overview

{Important!  Do not say in this section that this is college assignment.  Talk about what you are trying to accomplish as a software engineer to further your learning.}

{Provide a description the networking program that you wrote. Describe how to use your software.  If you did Client/Server, then you will need to describe how to start both.}

This project is a Peer-to-Peer (P2P) file-sharing application built using Python. The application allows peers to communicate directly and transfer files over a network using TCP sockets.

A tracker server is used to help peers discover one another, but actual file transfers occur directly between peers.

- Peer-to-peer communication
- TCP socket programming
- Request/response communication
- Multi-threading
- JSON-based messaging
- File transfer between computers

{Describe your purpose for writing this software.}

My purpose to write this project is to make it easy to transfer my files in my work area with my companions.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (you will need to show two pieces of software running and communicating with each other) and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

{Describe the architecture that you used (client/server or peer-to-peer)}

{Identify if you are using TCP or UDP and what port numbers are used.}

{Identify the format of messages being sent between the client and server or the messages sent between two peers.}

# Development Environment

{Describe the tools that you used to develop the software}

{Describe the programming language that you used and any libraries.}
I used Python to creates my program and also I used some libraries like, sockets.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Web Site Name](http://url.link.goes.here)
* [Web Site Name](http://url.link.goes.here)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* a conversation chat between users.
* a better gui that can have more options.
* video calling between users.