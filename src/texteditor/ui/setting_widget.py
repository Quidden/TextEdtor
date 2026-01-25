from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QTabWidget, \
    QTextEdit
from src.texteditor.ui.setting_tabs import \
    setting_menu_widget, \
    black_list_menu_widget


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QGroupBox("Settings")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.tab_widget = QTabWidget()

        self.black_list_menu = black_list_menu_widget.BlackListMenu()
        self.tab_widget.addTab(self.black_list_menu, "Black list")
        self.setting_menu = setting_menu_widget.SettingMenu()
        self.tab_widget.addTab(self.setting_menu, "Settings")
        self.log = QTextEdit()
        self.tab_widget.addTab(self.log, "Log")
        self.v_layout.addWidget(self.tab_widget)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.box)

    def get_tab_widget(self):
        return self.tab_widget
    def get_box(self):
        return self.box

    def get_log(self):
        return self.log
    def set_log(self, text):
        self.log.setPlainText(text)