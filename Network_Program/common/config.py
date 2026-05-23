from pathlib import Path

# ==================================================
# NETWORK SETTINGS
# ==================================================

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 9000

DEFAULT_PEER_HOST = "0.0.0.0"
DEFAULT_PEER_PORT = 5001

BUFFER_SIZE = 4096
ENCODING = "utf-8"

SOCKET_BACKLOG = 5


# ==================================================
# STORAGE PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PEER_DIR = BASE_DIR / "peer"

STORAGE_DIR = PEER_DIR / "storage"

SHARED_FOLDER = STORAGE_DIR / "shared"
DOWNLOAD_FOLDER = STORAGE_DIR / "downloads"
TEMP_FOLDER = STORAGE_DIR / "temp"


# ==================================================
# DOWNLOAD SETTINGS
# ==================================================

DOWNLOAD_CHUNK_SIZE = BUFFER_SIZE
DOWNLOAD_TIMEOUT = 10


# ==================================================
# GUI SETTINGS
# ==================================================

WINDOW_TITLE = "P2P File Sharing"

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

THEME_MODE = "dark"
COLOR_THEME = "blue"


# ==================================================
# PROTOCOL SETTINGS
# ==================================================

MAX_MESSAGE_SIZE = 1024 * 1024


# ==================================================
# CREATE DIRECTORIES
# ==================================================

SHARED_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

DOWNLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

TEMP_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)