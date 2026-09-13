from io import BytesIO

import qrcode
from PyQt6.QtCore import QThread, pyqtSignal

from texteditor.services.app_logger import get_logger
from texteditor.services.telegram import (
    TelegramError,
    check_telegram_account,
    complete_login,
    complete_password_login,
    delete_telegram_message,
    edit_telegram_message,
    login_with_qr,
    request_login_code,
    send_to_telegram,
    sync_telegram_messages,
)


logger = get_logger(__name__)


class TelegramSendWorker(QThread):
    sent = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, credentials, text, image_path, parent=None):
        super().__init__(parent)
        self.credentials = credentials
        self.text = text
        self.image_path = image_path

    def run(self):
        try:
            records = send_to_telegram(
                self.credentials,
                self.text,
                self.image_path,
            )
        except TelegramError as error:
            self.failed.emit(str(error))
        except Exception:
            logger.exception("Unexpected Telegram send error")
            self.failed.emit("Unexpected error while sending to Telegram.")
        else:
            self.sent.emit(records)


class TelegramCheckWorker(QThread):
    connected = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, credentials, parent=None):
        super().__init__(parent)
        self.credentials = credentials

    def run(self):
        try:
            check_telegram_account(self.credentials)
        except TelegramError as error:
            self.failed.emit(str(error))
        except Exception:
            logger.exception("Unexpected Telegram connection check error")
            self.failed.emit("Could not check Telegram account.")
        else:
            self.connected.emit()


class TelegramMessageActionWorker(QThread):
    succeeded = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, action, credentials, record_id, text="", parent=None):
        super().__init__(parent)
        self.action = action
        self.credentials = credentials
        self.record_id = record_id
        self.text = text

    def run(self):
        try:
            if self.action == "edit":
                edit_telegram_message(
                    self.credentials,
                    self.record_id,
                    self.text,
                )
                message = "Message updated in Telegram."
            else:
                delete_telegram_message(self.credentials, self.record_id)
                message = "Message deleted from Telegram."
        except TelegramError as error:
            self.failed.emit(str(error))
        except Exception:
            logger.exception("Unexpected Telegram message action error")
            self.failed.emit("Telegram operation failed.")
        else:
            self.succeeded.emit(message)


class TelegramMessagesSyncWorker(QThread):
    loaded = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, credentials, parent=None):
        super().__init__(parent)
        self.credentials = credentials

    def run(self):
        try:
            records = sync_telegram_messages(self.credentials, 30)
        except TelegramError as error:
            self.failed.emit(str(error))
        except Exception:
            logger.exception("Unexpected Telegram messages sync error")
            self.failed.emit("Could not load Telegram messages.")
        else:
            self.loaded.emit(records)


class TelegramAuthWorker(QThread):
    succeeded = pyqtSignal(str)
    failed = pyqtSignal(str)
    qr_ready = pyqtSignal(bytes)
    code_sent = pyqtSignal()
    password_required = pyqtSignal()

    def __init__(
            self,
            action,
            credentials,
            code="",
            password="",
            parent=None):
        super().__init__(parent)
        self.action = action
        self.credentials = credentials
        self.code = code
        self.password = password

    def run(self):
        try:
            if self.action == "request_code":
                result = request_login_code(self.credentials)
                message = result["message"]
                if result["status"] == "code_sent":
                    self.code_sent.emit()
            elif self.action == "sign_in":
                if self.code:
                    complete_login(
                        self.credentials,
                        self.code,
                        self.password,
                    )
                else:
                    complete_password_login(
                        self.credentials,
                        self.password,
                    )
                message = "Telegram account signed in."
            else:
                login_with_qr(
                    self.credentials,
                    self.emit_qr_code,
                    self.password,
                )
                message = "Telegram account signed in with QR code."
        except TelegramError as error:
            if "2FA password" in str(error) or "cloud password" in str(error):
                self.password_required.emit()
            self.failed.emit(str(error))
        except Exception:
            logger.exception("Unexpected Telegram authorization error")
            self.failed.emit("Telegram authorization failed.")
        else:
            self.succeeded.emit(message)

    def emit_qr_code(self, url):
        qr_image = qrcode.make(url)
        image_buffer = BytesIO()
        qr_image.save(image_buffer, format="PNG")
        self.qr_ready.emit(image_buffer.getvalue())
