from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QHBoxLayout, \
    QTextEdit, \
    QPushButton, \
    QLabel
import pyperclip
from PyQt6.QtCore import pyqtSignal

from texteditor.services.app_logger import \
    get_logger


logger = get_logger(__name__)


class ResultWidget(QWidget):
    push_to_telegram_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.box = QGroupBox()
        self.v_head_box_layout = QVBoxLayout()
        self.box.setLayout(self.v_head_box_layout)

        self.h_head_layout = QHBoxLayout()

        self.result_text = QTextEdit()
        self.v_head_box_layout.addWidget(self.result_text)
        self.v_head_box_layout.addLayout(self.h_head_layout)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_text)
        self.h_head_layout.addWidget(self.copy_button)
        self.telegram_button = QPushButton("Push to TG")
        self.telegram_button.clicked.connect(
            self.request_telegram_send
        )
        self.h_head_layout.addWidget(self.telegram_button)
        self.tech_button = QPushButton("Tech")
        self.tech_button.setVisible(False)
        self.h_head_layout.addWidget(self.tech_button)
        self.tech_button2 = QPushButton("Tech2")
        self.tech_button2.setVisible(False)
        self.h_head_layout.addWidget(self.tech_button2)

        self.telegram_status = QLabel()
        self.telegram_status.setObjectName("StatusDot")
        self.telegram_status.setFixedSize(10, 10)
        self.telegram_status.setToolTip("Not sent")
        self.set_telegram_status("idle")
        self.telegram_status_text = QLabel("Telegram: not sent")
        self.telegram_status_text.setObjectName("StatusText")
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.telegram_status)
        status_layout.addWidget(self.telegram_status_text)
        status_layout.addStretch()
        self.v_head_box_layout.addLayout(status_layout)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.box)

    def get_text(self):
        return self.result_text.toPlainText()

    def set_text(self, text):
        self.result_text.setPlainText(text)

    def get_copy_button(self):
        return self.copy_button

    def copy_text(self):
        try:
            pyperclip.copy(self.result_text.toPlainText())
        except pyperclip.PyperclipException as error:
            logger.error("Result text copy failed: %s", error)
            return

        logger.info("Result text copied")

    def request_telegram_send(self):
        self.set_telegram_status("sending")
        self.push_to_telegram_requested.emit(self.get_text())

    def set_telegram_status(self, status, message=None):
        colors = {
            "idle": "#050505",
            "sending": "#f5c542",
            "sent": "#35c759",
        }
        tooltips = {
            "idle": "Not sent",
            "sending": "Sending to Telegram",
            "sent": "Sent to Telegram",
        }
        labels = {
            "idle": "Telegram: not sent",
            "sending": "Telegram: sending",
            "sent": "Telegram: sent",
        }
        color = colors.get(status, colors["idle"])
        self.telegram_status.setStyleSheet(
            f"background-color: {color}; border: 1px solid #5b5868; "
            "border-radius: 5px;"
        )
        status_message = message or tooltips.get(status, "Not sent")
        self.telegram_status.setToolTip(status_message)
        if hasattr(self, "telegram_status_text"):
            self.telegram_status_text.setText(labels.get(status, labels["idle"]))
            self.telegram_status_text.setToolTip(status_message)

    def get_tech_button(self):
        return self.tech_button

    def get_tech_button2(self):
        return self.tech_button2
