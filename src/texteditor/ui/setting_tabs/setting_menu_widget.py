from PyQt6.QtCore import \
    Qt
from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QCheckBox, \
    QPushButton, \
    QHBoxLayout

from src.texteditor.services.save_func import \
    save_settings, \
    load_settings


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

        if load_settings():
            for key, value in load_settings().items():
                if key == "empty_text_settings":
                    self.check_box_text_empty_settings.setChecked(value)
                if key == "text_settings":
                    self.check_box_text_settings.setChecked(value)

        self.h_button_save_layout = QHBoxLayout()
        self.button_save = QPushButton("Save settings")
        self.button_save.clicked.connect(lambda: save_settings(
            text_settings=self.check_box_text_settings.isChecked(),
            empty_text_settings=self.check_box_text_empty_settings.isChecked(),
        ))
        self.h_button_save_layout.addWidget(self.button_save)
        self.v_layout.addLayout(self.h_button_save_layout)

        self.v_main_layout = QVBoxLayout()
        self.v_main_layout.addWidget(self.box)
        self.setLayout(self.v_main_layout)

    def get_check_box_text_settings(self):
        return self.check_box_text_settings.isChecked()
    def get_check_box_text_empty_settings(self):
        return self.check_box_text_empty_settings.isChecked()
