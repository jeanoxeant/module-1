import json


# ==========================================
# MESSAGE TYPES
# ==========================================

REGISTER = "register"
SEARCH = "search"
LIST = "list"
DOWNLOAD = "download"
PING = "ping"
ERROR = "error"


# ==========================================
# REQUEST BUILDERS
# ==========================================

def create_register_request(
    peer_id,
    ip,
    port,
    files
):
    """
    Create register request.
    """

    return {
        "type": REGISTER,
        "peer_id": peer_id,
        "ip": ip,
        "port": port,
        "files": files
    }


def create_search_request(
    filename
):
    """
    Create search request.
    """

    return {
        "type": SEARCH,
        "filename": filename
    }


def create_list_request():
    """
    Create request to list all shared files.
    """

    return {
        "type": LIST
    }


def create_download_request(
    filename
):
    """
    Create download request.
    """

    return {
        "type": DOWNLOAD,
        "filename": filename
    }


def create_ping_request():
    """
    Create ping request.
    """

    return {
        "type": PING
    }


# ==========================================
# RESPONSE BUILDERS
# ==========================================

def create_success_response(
    message="success",
    data=None
):
    """
    Create success response.
    """

    response = {
        "status": "success",
        "message": message
    }

    if data is not None:
        response["data"] = data

    return response


def create_error_response(
    message
):
    """
    Create error response.
    """

    return {
        "status": "error",
        "message": message
    }


def create_search_response(
    results
):
    """
    Create search results response.
    """

    return {
        "status": "success",
        "results": results
    }


# ==========================================
# SERIALIZATION
# ==========================================

def encode_message(
    message,
    encoding="utf-8"
):
    """
    Convert dict -> bytes.
    """

    return json.dumps(
        message
    ).encode(encoding)


def decode_message(
    data,
    encoding="utf-8"
):
    """
    Convert bytes -> dict.
    """

    return json.loads(
        data.decode(encoding)
    )