from ..config import \
    SAVE_SETTINGS_FILE, \
    DATA_DIR

import json
import os

def save_settings(
        *,
        text_settings,
        empty_text_settings,
        telegram_api_id="",
        telegram_api_hash="",
        telegram_phone=""):

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except OSError:
        return "mkdir error"

    try:
        if not os.path.exists(
                SAVE_SETTINGS_FILE):
            with open(
                    SAVE_SETTINGS_FILE, "w") as outfile:
                json.dump([],outfile)
    except OSError:
        return "create json error"

    settings = {
        "text_settings": text_settings,
        "empty_text_settings": empty_text_settings,
        "telegram_api_id": telegram_api_id,
        "telegram_api_hash": telegram_api_hash,
        "telegram_phone": telegram_phone,
    }

    json_object = json.dumps(settings, indent=4, sort_keys=True, ensure_ascii=False)

    try:
        with open(
            SAVE_SETTINGS_FILE, "w") as outfile:
            outfile.write(json_object)
    except OSError:
        return "write json error"

    return True


def load_settings():
    settings = {}
    if not os.path.exists(SAVE_SETTINGS_FILE):
        return False

    try:
        with open(
                SAVE_SETTINGS_FILE, "r") as infile:
            settings = json.load(infile)
    except (OSError, json.JSONDecodeError):
        return False

    if isinstance(settings, dict) and "telegram_bot_token" in settings:
        settings.pop("telegram_bot_token", None)
        try:
            with open(SAVE_SETTINGS_FILE, "w", encoding="utf-8") as outfile:
                json.dump(
                    settings,
                    outfile,
                    indent=4,
                    sort_keys=True,
                    ensure_ascii=False,
                )
        except OSError:
            pass
    return settings
