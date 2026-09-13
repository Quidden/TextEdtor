from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TelegramAuthWidget(QWidget):
    def __init__(self, settings=None, parent=None):
        super().__init__(parent)
        settings = settings or {}

        self.phone_code_sent = False
        self.password_required = False

        self.box = QGroupBox("Telegram account")
        layout = QVBoxLayout(self.box)

        self.api_id = QLineEdit()
        self.api_id.setPlaceholderText("Telegram API ID")
        self.api_id.setText(str(settings.get("telegram_api_id", "")))
        layout.addWidget(self.api_id)

        self.api_hash = QLineEdit()
        self.api_hash.setPlaceholderText("Telegram API hash")
        self.api_hash.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_hash.setText(settings.get("telegram_api_hash", ""))
        layout.addWidget(self.api_hash)

        self.login_mode = QComboBox()
        self.login_mode.addItem("QR code", "qr")
        self.login_mode.addItem("Phone and code", "phone")
        layout.addWidget(self.login_mode)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("+380...")
        self.phone.setText(settings.get("telegram_phone", ""))
        layout.addWidget(self.phone)

        self.send_code_button = QPushButton("Send code")
        layout.addWidget(self.send_code_button)

        self.code = QLineEdit()
        self.code.setPlaceholderText("Login code from Telegram")
        layout.addWidget(self.code)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password for your Telegram account")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        self.sign_in_button = QPushButton("Sign in")
        layout.addWidget(self.sign_in_button)

        self.qr_login_button = QPushButton("Generate QR code")
        layout.addWidget(self.qr_login_button)

        self.qr_image = QLabel()
        self.qr_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_image.setVisible(False)
        layout.addWidget(self.qr_image)

        self.auth_status = QLabel("Telegram account: not signed in")
        self.auth_status.setObjectName("StatusText")
        self.auth_status.setWordWrap(True)
        layout.addWidget(self.auth_status)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.box)

        self.login_mode.currentIndexChanged.connect(self.update_login_mode)
        self.update_login_mode()

    def credentials(self):
        return {
            "api_id": self.api_id.text().strip(),
            "api_hash": self.api_hash.text().strip(),
            "phone": self.phone.text().strip(),
        }

    def login_code(self):
        return self.code.text().strip()

    def cloud_password(self):
        return self.password.text()

    def current_login_mode(self):
        return self.login_mode.currentData()

    def update_login_mode(self):
        phone_mode = self.current_login_mode() == "phone"
        self.phone.setVisible(phone_mode)
        self.send_code_button.setVisible(
            phone_mode and not self.phone_code_sent
        )
        self.code.setVisible(phone_mode and self.phone_code_sent)
        self.qr_login_button.setVisible(not phone_mode)
        self.qr_image.setVisible(
            not phone_mode and not self.qr_image.pixmap().isNull()
        )
        self.password.setVisible(self.password_required)
        self.sign_in_button.setVisible(
            self.password_required
            or (phone_mode and self.phone_code_sent)
        )

    def show_code_step(self):
        self.phone_code_sent = True
        self.password_required = False
        self.update_login_mode()
        self.code.setFocus()

    def show_password_step(self):
        self.password_required = True
        self.update_login_mode()
        self.password.setFocus()

    def reset_steps(self):
        self.phone_code_sent = False
        self.password_required = False
        self.code.clear()
        self.password.clear()
        self.clear_qr_code()
        self.update_login_mode()

    def set_status(self, message, success=False):
        color = "#35c759" if success else "#aaa4bb"
        self.auth_status.setStyleSheet(f"color: {color};")
        self.auth_status.setText(message)

    def set_qr_code(self, image_bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(image_bytes, "PNG")
        self.qr_image.setPixmap(pixmap)
        self.update_login_mode()

    def clear_qr_code(self):
        self.qr_image.clear()
        self.qr_image.setVisible(False)
