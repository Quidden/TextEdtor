import os

from PyQt6.QtCore import \
    QFileSystemWatcher, \
    QTimer
from PyQt6.QtGui import \
    QTextCursor
from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QHBoxLayout, \
    QPushButton, \
    QTabWidget, \
    QTextEdit
from texteditor.config import \
    APP_LOG_FILE, \
    DATA_DIR
from texteditor.ui.setting_tabs import \
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
        self.log.setReadOnly(True)
        self.log.setObjectName("LogText")
        self.set_log(self.load_log_text())

        self.log_tab = QWidget()
        self.log_layout = QVBoxLayout(self.log_tab)
        self.log_layout.setContentsMargins(8, 8, 8, 8)
        self.log_layout.setSpacing(8)
        self.refresh_log_button = QPushButton("Refresh log")
        self.refresh_log_button.clicked.connect(self.refresh_log)
        self.log_button_layout = QHBoxLayout()
        self.log_button_layout.addStretch()
        self.log_button_layout.addWidget(self.refresh_log_button)
        self.log_layout.addLayout(self.log_button_layout)
        self.log_layout.addWidget(self.log)

        self.tab_widget.addTab(self.log_tab, "Log")
        self.tab_widget.currentChanged.connect(self.refresh_log_tab)
        self.v_layout.addWidget(self.tab_widget)

        self.log_watcher = QFileSystemWatcher(self)
        self.ensure_log_file()
        self.log_watcher.addPath(APP_LOG_FILE)
        self.log_watcher.fileChanged.connect(self.refresh_log_from_watcher)

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
        self.log.moveCursor(QTextCursor.MoveOperation.End)

    def load_log_text(self):
        try:
            with open(APP_LOG_FILE, "r", encoding="utf-8") as log_file:
                return log_file.read()
        except FileNotFoundError:
            return "Log file was not found."
        except UnicodeDecodeError:
            with open(APP_LOG_FILE, "r", encoding="cp1251", errors="replace") as log_file:
                return log_file.read()

    def refresh_log_tab(self, index):
        if self.tab_widget.widget(index) == self.log_tab:
            self.refresh_log()

    def refresh_log(self):
        self.set_log(self.load_log_text())

    def refresh_log_from_watcher(self):
        self.refresh_log()
        QTimer.singleShot(100, self.restore_log_watcher)

    def restore_log_watcher(self):
        if APP_LOG_FILE not in self.log_watcher.files() and os.path.exists(APP_LOG_FILE):
            self.log_watcher.addPath(APP_LOG_FILE)

    def ensure_log_file(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(APP_LOG_FILE):
            with open(APP_LOG_FILE, "w", encoding="utf-8"):
                pass
