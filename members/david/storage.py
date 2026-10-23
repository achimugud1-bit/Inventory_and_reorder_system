'David: read and safely save the shared inventory file.'

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "members/cynthia/data.json"


def load_inventory():
    'Read the current inventory from Cynthia shared data file.'
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_inventory(data):
    'Write to a temporary file, then replace the saved inventory.'
    temp_file = DATA_FILE.with_suffix(".json.tmp")
    temp_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "
",
        encoding="utf-8",
    )
    temp_file.replace(DATA_FILE)
