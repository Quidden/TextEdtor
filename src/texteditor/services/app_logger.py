import logging
import os

from src.texteditor.config import APP_LOG_FILE, DATA_DIR


def setup_logging():
    os.makedirs(DATA_DIR, exist_ok=True)

    logging.basicConfig(
        filename=APP_LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
        force=True,
    )

    logging.getLogger("texteditor").info("Application started")


def get_logger(name):
    return logging.getLogger(f"texteditor.{name}")
