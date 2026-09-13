from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QPushButton, \
    QLabel, \
    QHBoxLayout


class GenButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QGroupBox("General Buttons")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.button1 = QPushButton("Accept black list")
        self.button2 = QPushButton("Split text")
        self.button3 = QPushButton("Button3")
        self.button4 = QPushButton("Button4")
        self.button5 = QPushButton("Button5")
        self.button6 = QPushButton("Button6")
        self.button3.setText("Telegram manager")
        self.button3.setVisible(True)
        self.button4.setVisible(False)
        self.button5.setVisible(False)
        self.button6.setVisible(False)

        self.v_layout.addWidget(self.button1)
        self.v_layout.addWidget(self.button2)
        self.v_layout.addWidget(self.button3)
        self.v_layout.addWidget(self.button4)
        self.v_layout.addWidget(self.button5)
        self.v_layout.addWidget(self.button6)

        self.telegram_status = QLabel()
        self.telegram_status.setObjectName("StatusDot")
        self.telegram_status.setFixedSize(10, 10)
        self.telegram_status_text = QLabel("Telegram account: not signed in")
        self.telegram_status_text.setObjectName("StatusText")
        self.telegram_status_layout = QHBoxLayout()
        self.telegram_status_layout.addWidget(self.telegram_status)
        self.telegram_status_layout.addWidget(self.telegram_status_text)
        self.telegram_status_layout.addStretch()
        self.v_layout.addLayout(self.telegram_status_layout)
        self.set_telegram_status("disconnected")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.box)

    def buttons(self):
        return self.button1, self.button2, self.button3, self.button4, self.button5, self.button6

    def set_telegram_status(self, status, message=None):
        states = {
            "disconnected": ("#050505", "Telegram account: not signed in"),
            "checking": ("#f5c542", "Telegram account: checking"),
            "connected": ("#35c759", "Telegram account: connected"),
        }
        color, default_message = states.get(status, states["disconnected"])
        status_message = message or default_message
        self.telegram_status.setStyleSheet(
            f"background-color: {color}; border: 1px solid #5b5868; "
            "border-radius: 5px;"
        )
        self.telegram_status.setToolTip(status_message)
        self.telegram_status_text.setText(status_message)
