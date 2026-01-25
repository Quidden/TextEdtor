from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QHBoxLayout, \
    QTextEdit, \
    QPushButton


class ResultWidget(QWidget):
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
        self.h_head_layout.addWidget(self.copy_button)
        self.tech_button = QPushButton("Tech")
        self.tech_button.setVisible(False)
        self.h_head_layout.addWidget(self.tech_button)
        self.tech_button2 = QPushButton("Tech2")
        self.tech_button2.setVisible(False)
        self.h_head_layout.addWidget(self.tech_button2)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.box)

    def get_text(self):
        return self.result_text.toPlainText()

    def set_text(self, text):
        self.result_text.setPlainText(text)

    def get_copy_button(self):
        return self.copy_button

    def get_tech_button(self):
        return self.tech_button

    def get_tech_button2(self):
        return self.tech_button2