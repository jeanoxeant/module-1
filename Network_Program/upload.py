import os
import shutil

from common.config import (
    SHARED_FOLDER,
)


def upload_file(filepath):
    """Copy a selected file into the shared folder."""
    if not filepath:
        raise ValueError("No file selected")

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    os.makedirs(SHARED_FOLDER, exist_ok=True)

    filename = os.path.basename(filepath)
    destination = os.path.join(SHARED_FOLDER, filename)

    shutil.copy2(filepath, destination)

    return filename, destination
