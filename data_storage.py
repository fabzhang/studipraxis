import json
from pathlib import Path

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_data(file_path):
    if Path(file_path).exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []
