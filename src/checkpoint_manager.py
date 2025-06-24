
import json
import os

CHECKPOINT_FILE = os.path.join("checkpoint", "last_read.json")

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return 0
    try:
        with open(CHECKPOINT_FILE, "r") as file:
            data = json.load(file)
            return data.get("last_read_row", 0)
    except json.JSONDecodeError:
        return 0

def save_checkpoint(row_number):
    with open(CHECKPOINT_FILE, "w") as file:
        json.dump({"last_read_row": row_number}, file)

