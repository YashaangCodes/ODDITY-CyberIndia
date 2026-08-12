import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "phone_reputation.json"
)


def load_phone_reputation_data() -> list[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("records", [])
