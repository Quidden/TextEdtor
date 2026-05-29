from PyQt6.QtCore import \
    Qt
from PyQt6.QtWidgets import \
    QWidget, \
    QListWidget, \
    QPushButton, \
    QHBoxLayout, \
    QVBoxLayout, \
    QGroupBox, \
    QLabel, \
    QLineEdit, \
    QMenu

from texteditor.services.black_list import \
    refresh_black_list, \
    black_list_item_delete
from texteditor.services.app_logger import \
    get_logger


logger = get_logger(__name__)


class BlackListMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.b_list = QListWidget()

        for item in refresh_black_list():
            self.b_list.addItem(str(item))
        self.b_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.b_list.customContextMenuRequested.connect(self.open_menu)

        self.refresh_button = QPushButton("Refresh")
        self.delete_item = QPushButton("Delete")
        self.refresh_button.setVisible(False)
        self.delete_item.setVisible(False)
        self.h_button_layout = QHBoxLayout()
        self.h_button_layout.addWidget(self.refresh_button)
        self.h_button_layout.addWidget(self.delete_item)

        self.v2_widget = QWidget()
        self.v2_layout = QVBoxLayout(self.v2_widget)
        self.v2_layout.addWidget(self.b_list)
        self.v2_layout.addLayout(self.h_button_layout)

        self.second_box = QGroupBox("Black list add item tab")
        self.v3_layout = QVBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.black_list_item = QLineEdit()
        self.black_list_item.setPlaceholderText("Blacklist Item")
        self.white_list_item = QLineEdit()
        self.white_list_item.setPlaceholderText("Whitelist Item")

        self.h2_layout.addWidget(self.black_list_item)
        self.h2_layout.addWidget(QLabel("->"))
        self.h2_layout.addWidget(self.white_list_item)
        self.v3_layout.addLayout(self.h2_layout)

        self.confirm_button = QPushButton("Confirm")
        self.v3_layout.addWidget(self.confirm_button)

        self.second_box.setLayout(self.v3_layout)
        self.v2_layout.addWidget(self.second_box)

        self.setLayout(self.v2_layout)


    def open_menu(self, position):
        item = self.b_list.itemAt(position)

        menu = QMenu(self)

        delete = menu.addAction("Delete")
        action = menu.exec(self.b_list.mapToGlobal(position))
        if action == delete:
            black_list_item_delete(self.b_list.row(item))
            logger.info("Black list item deleted: %s", item.text())
            self.clear_black_list()
            for item in refresh_black_list():
                self.b_list.addItem(str(item))

    def get_black_list(self):
        return self.b_list
    def add_black_list_item(self, text):
        self.b_list.addItem(text)
    def clear_black_list(self):
        self.b_list.clear()

    def get_black_list_item(self):
        return self.black_list_item
    def get_white_list_item(self):
        return self.white_list_item
    def get_confirm_button(self):
        return self.confirm_button

    def get_refresh_button(self):
        return self.refresh_button
