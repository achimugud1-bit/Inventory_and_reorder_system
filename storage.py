"""Read and safely save the shared inventory JSON file."""

import json
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MEMBERS = ROOT / "members"
DATA_FILE = next(MEMBERS.glob("*/data.json"))
DATA_LOCK = threading.Lock()


def load_data():
    """Load the latest inventory while holding the shared data lock."""
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data):
    """Write a temporary file, then replace the inventory in one step."""
    temp_file = DATA_FILE.with_suffix(".json.tmp")
    temp_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temp_file.replace(DATA_FILE)
