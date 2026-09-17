import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

IS_DOCKER = bool(os.environ.get("DOCKER"))

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]


def _storage_path():
    storage_path = Path(os.environ["STORAGE_PATH"])

    if not storage_path.exists():
        storage_path.mkdir()

    if not IS_DOCKER:
        (storage_path / ".gitignore").write_text("*")

    return storage_path


STORAGE_PATH = _storage_path()
IMAGE_PATH = STORAGE_PATH / "images"
THUMB_PATH = STORAGE_PATH / "thumbs"
