from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from texteditor.services.app_logger import get_logger
from texteditor.services.black_list import (
    accept_black_list,
    black_list_load,
    refresh_black_list,
)
from texteditor.services.text_edit import text_division
from texteditor.ui.get_button_widget import GenButtons
from texteditor.ui.image_result_widget import ImageResult
from texteditor.ui.result_widget import ResultWidget
from texteditor.ui.setting_widget import SettingsTab
from texteditor.ui.telegram_controller import TelegramControllerMixin
from texteditor.ui.telegram_manager_widget import TelegramManagerWidget
from texteditor.ui.text_widget import TextWidget


logger = get_logger(__name__)


class MainWindowW(TelegramControllerMixin, QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.page_stack = QStackedWidget()
        self.main_layout.addWidget(self.page_stack)

        self.main_page = QWidget()
        self.page_stack.addWidget(self.main_page)

        self.h_head_layout = QHBoxLayout()
        self.h_head_layout.setContentsMargins(14, 14, 14, 14)
        self.h_head_layout.setSpacing(12)
        self.main_page.setLayout(self.h_head_layout)

        self.v_text_result_layout = QVBoxLayout()
        self.v_text_result_layout.setSpacing(10)
        self.ImageResult = ImageResult()
        self.v_text_result_layout.addWidget(self.ImageResult)
        self.h_head_layout.addLayout(self.v_text_result_layout, 2)

        self.main_text = QVBoxLayout()
        self.main_text.setSpacing(10)
        self.TextWidget = TextWidget()
        self.main_text.addWidget(self.TextWidget)
        self.h_head_layout.addLayout(self.main_text, 4)

        self.v_settings_layout = QVBoxLayout()
        self.v_settings_layout.setSpacing(10)
        self.SettingsTab = SettingsTab()
        self.v_settings_layout.addWidget(self.SettingsTab)
        self.SettingsTab.black_list_menu.confirm_button.clicked.connect(
            lambda: self.bl_list_func()
        )

        self.GenButtons = GenButtons()
        self.v_settings_layout.addWidget(self.GenButtons)
        self.but = self.GenButtons.buttons()
        self.but[0].clicked.connect(self.replace_text)
        self.but[1].clicked.connect(self.text_division_result)
        self.h_head_layout.addLayout(self.v_settings_layout, 2)

        self.TelegramManager = TelegramManagerWidget()
        self.TelegramManager.black_list_menu.confirm_button.clicked.connect(
            lambda: self.bl_list_func(self.TelegramManager.black_list_menu)
        )
        self.page_stack.addWidget(self.TelegramManager)

        self.setup_telegram_controller()

    def bl_list_func(self, menu=None):
        menu = menu or self.SettingsTab.black_list_menu
        black_list_text = menu.black_list_item.text()
        white_list_text = menu.white_list_item.text()

        result = black_list_load(
            black_list=black_list_text,
            white_list=white_list_text,
        )
        if result is not True:
            logger.warning("Black list item was not added: duplicate or invalid value")
            self.msg_box = QMessageBox()
            self.setWindowTitle("Error")
            self.msg_box.setText("Replace")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg_box.exec()
            return

        logger.info("Black list item added: %s -> %s", black_list_text, white_list_text)
        menu.clear_black_list()
        for item in refresh_black_list():
            menu.add_black_list_item(str(item))

    def replace_text(self):
        logger.info("Applying text replacement settings")
        self.TextWidget.set_general_text(
            accept_black_list(
                self.TextWidget.get_general_text(),
                self.SettingsTab.setting_menu.get_check_box_text_settings(),
                self.SettingsTab.setting_menu.get_check_box_text_empty_settings(),
            )
        )

    def get_text_widget(self):
        return self.TextWidget

    def text_division_result(self):
        logger.info("Splitting text into result blocks")
        for result_box in self.findChildren(ResultWidget):
            result_box.setParent(None)
            result_box.deleteLater()

        for text_block in text_division(self.TextWidget.get_general_text()):
            result_box = ResultWidget()
            result_box.set_text(text_block)
            self.connect_result_to_telegram(result_box)
            self.v_text_result_layout.addWidget(result_box)
