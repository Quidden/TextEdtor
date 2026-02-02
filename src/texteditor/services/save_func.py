from ..config import \
    SAVE_SETTINGS_FILE, \
    DATA_DIR

import json
import os

def save_settings(*, text_settings, empty_text_settings):

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except:
        return "mkdir error"

    try:
        if not os.path.exists(
                SAVE_SETTINGS_FILE):
            with open(
                    SAVE_SETTINGS_FILE, "w") as outfile:
                json.dump([],outfile)
    except:
        return "create json error"

    settings = {
        "Text settings": text_settings,
        "Empty text settings": empty_text_settings
    }

    json_object = json.dumps(settings, indent=4, sort_keys=True, ensure_ascii=False)

    try:
        with open(
            SAVE_SETTINGS_FILE, "w") as outfile:
            outfile.write(json_object)
    except:
        return "write json error"

    return True


def load_settings():
    settings = {}
    if not os.path.exists(SAVE_SETTINGS_FILE):
        return False

    with open(
            SAVE_SETTINGS_FILE, "r") as infile:
        settings = json.load(infile)
    return settings