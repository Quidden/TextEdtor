from PyQt6.QtCore import \
    Qt
from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QCheckBox


class SettingMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QGroupBox("Settings")
        self.v_layout = QVBoxLayout()
        self.v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.box.setLayout(self.v_layout)

        self.check_box_text_settings = QCheckBox("Text settings")
        self.v_layout.addWidget(self.check_box_text_settings)
        self.check_box_text_empty_settings = QCheckBox("Empty text settings")
        self.v_layout.addWidget(self.check_box_text_empty_settings)


        self.v_main_layout = QVBoxLayout()
        self.v_main_layout.addWidget(self.box)
        self.setLayout(self.v_main_layout)

    def get_check_box_text_settings(self):
        return self.check_box_text_settings.isChecked()
    def get_check_box_text_empty_settings(self):
        return self.check_box_text_empty_settings.isChecked()