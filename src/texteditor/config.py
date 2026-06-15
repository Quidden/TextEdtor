import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT_DIR, "data")
BLACK_LIST_FILE = os.path.join(DATA_DIR, "black_list.json")
SAVE_SETTINGS_FILE = os.path.join(DATA_DIR, "save_settings.json")
APP_LOG_FILE = os.path.join(DATA_DIR, "app.log")
TELEGRAM_STATE_FILE = os.path.join(DATA_DIR, "telegram_state.json")
TELEGRAM_MESSAGES_FILE = os.path.join(DATA_DIR, "telegram_messages.json")
TELEGRAM_SESSION_FILE = os.path.join(DATA_DIR, "telegram_user")
TELEGRAM_LOGIN_STATE_FILE = os.path.join(DATA_DIR, "telegram_login.json")
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
