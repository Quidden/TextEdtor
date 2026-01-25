from ..config import \
    SAVE_SETTINGS_FILE, \
    DATA_DIR

import json
import os

def save_settings(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    temp = []
    if not os.path.exists(
            SAVE_SETTINGS_FILE):
        with open(
                SAVE_SETTINGS_FILE, "w") as outfile:
            json.dump([],outfile)

    text_settings = False
    empty_text_settings = False

    settings = {
        "Text settings": text_settings,
        "Empty text settings": empty_text_settings
    }