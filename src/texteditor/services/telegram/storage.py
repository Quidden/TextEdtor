import json
import os

from texteditor.config import DATA_DIR
from texteditor.services.telegram.errors import TelegramError


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as source_file:
            return json.load(source_file)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path, value):
    os.makedirs(DATA_DIR, exist_ok=True)
    temporary_path = f"{path}.tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as target_file:
            json.dump(value, target_file, indent=4, ensure_ascii=False)
        os.replace(temporary_path, path)
    except OSError as error:
        raise TelegramError(f"Could not save Telegram state: {error}") from error
