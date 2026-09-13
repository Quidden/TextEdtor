from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from texteditor.services.app_logger import get_logger
from texteditor.services.save_func import load_settings, save_settings
from texteditor.ui.telegram_auth_widget import TelegramAuthWidget


logger = get_logger(__name__)


class SettingMenu(QWidget):
    def __init__(self):
        super().__init__()
        settings = load_settings() or {}

        self.box = QGroupBox("Settings")
        self.v_layout = QVBoxLayout(self.box)
        self.v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.check_box_text_settings = QCheckBox("Text settings")
        self.check_box_text_settings.setChecked(
            bool(settings.get("text_settings"))
        )
        self.v_layout.addWidget(self.check_box_text_settings)

        self.check_box_text_empty_settings = QCheckBox("Empty text settings")
        self.check_box_text_empty_settings.setChecked(
            bool(settings.get("empty_text_settings"))
        )
        self.v_layout.addWidget(self.check_box_text_empty_settings)

        self.telegram_auth = TelegramAuthWidget(settings)
        self.v_layout.addWidget(self.telegram_auth)

        self.h_button_save_layout = QHBoxLayout()
        self.button_save = QPushButton("Save settings")
        self.button_save.clicked.connect(self.save)
        self.h_button_save_layout.addWidget(self.button_save)
        self.v_layout.addLayout(self.h_button_save_layout)

        self.v_main_layout = QVBoxLayout(self)
        self.v_main_layout.addWidget(self.box)

    def save(self):
        credentials = self.telegram_auth.credentials()
        save_settings(
            text_settings=self.check_box_text_settings.isChecked(),
            empty_text_settings=self.check_box_text_empty_settings.isChecked(),
            telegram_api_id=credentials["api_id"],
            telegram_api_hash=credentials["api_hash"],
            telegram_phone=credentials["phone"],
        )
        logger.info("Settings saved")

    def get_check_box_text_settings(self):
        return self.check_box_text_settings.isChecked()

    def get_check_box_text_empty_settings(self):
        return self.check_box_text_empty_settings.isChecked()

    def get_telegram_credentials(self):
        return self.telegram_auth.credentials()

    def get_telegram_login_code(self):
        return self.telegram_auth.login_code()

    def get_telegram_password(self):
        return self.telegram_auth.cloud_password()

    def set_telegram_auth_status(self, message, success=False):
        self.telegram_auth.set_status(message, success)

    def set_telegram_qr_code(self, image_bytes):
        self.telegram_auth.set_qr_code(image_bytes)

    def clear_telegram_qr_code(self):
        self.telegram_auth.clear_qr_code()

    def show_telegram_code_step(self):
        self.telegram_auth.show_code_step()

    def show_telegram_password_step(self):
        self.telegram_auth.show_password_step()

    def reset_telegram_auth_steps(self):
        self.telegram_auth.reset_steps()
