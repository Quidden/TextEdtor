from PyQt6.QtWidgets import (
    QComboBox,
    QCheckBox,
    QGraphicsOpacityEffect,
    QLabel,
    QPushButton,
    QScrollArea,
    QSplitter,
    QLayout,
    QHBoxLayout,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from texteditor.ui.themes import THEMES, apply_theme, appearance_settings
from texteditor.ui.animated_border import AnimatedBorder

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
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.preferences = appearance_settings()
        self.header = QWidget()
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 12, 20, 8)
        brand = QLabel("textedtor")
        brand.setObjectName("Brand")
        header_layout.addWidget(brand)
        subtitle = QLabel("Paper Focus")
        subtitle.setObjectName("Subtitle")
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        self.theme_picker = QComboBox()
        for key, values in THEMES.items():
            self.theme_picker.addItem(values[0], key)
        selected = self.preferences.value("theme", "paper")
        self.theme_picker.setCurrentIndex(max(0, self.theme_picker.findData(selected)))
        self.theme_picker.currentIndexChanged.connect(self.change_theme)
        header_layout.addWidget(self.theme_picker)
        self.motion_toggle = QCheckBox("Анимации")
        self.motion_toggle.setChecked(self.preferences.value("animations", True, type=bool))
        self.motion_toggle.toggled.connect(lambda value: self.preferences.setValue("animations", value))
        header_layout.addWidget(self.motion_toggle)
        self.main_layout.addWidget(self.header)
        self.page_stack = QStackedWidget()
        self.main_layout.addWidget(self.page_stack)

        self.main_page = QWidget()
        self.page_stack.addWidget(self.main_page)

        self.h_head_layout = QHBoxLayout()
        self.h_head_layout.setContentsMargins(14, 14, 14, 14)
        self.h_head_layout.setSpacing(12)
        self.main_page.setLayout(self.h_head_layout)

        self.sidebar = QWidget()
        self.sidebar.setMaximumWidth(300)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.ImageResult = ImageResult()
        sidebar_layout.addWidget(self.ImageResult)
        self.h_head_layout.addWidget(self.sidebar, 1)

        self.main_text = QVBoxLayout()
        self.main_text.setSpacing(10)
        self.TextWidget = TextWidget()
        self.TextWidget.GeneralText.setObjectName("SourceEditor")
        self.source_border = AnimatedBorder(self.TextWidget.GeneralText, self.motion_toggle.isChecked())
        self.main_text.addWidget(self.TextWidget)
        self.editor_area = QWidget()
        self.editor_area.setLayout(self.main_text)
        self.results_area = QScrollArea()
        self.results_area.setWidgetResizable(True)
        self.results_content = QWidget()
        self.v_text_result_layout = QHBoxLayout(self.results_content)
        self.results_area.setWidget(self.results_content)
        self.empty_results = QLabel("Результаты появятся после разделения текста по =====")
        self.empty_results.setWordWrap(True)
        self.v_text_result_layout.addWidget(self.empty_results)
        self.editor_splitter = QSplitter(Qt.Orientation.Vertical)
        self.editor_splitter.addWidget(self.editor_area)
        self.editor_splitter.addWidget(self.results_area)
        self.editor_splitter.setSizes([430, 230])
        self.results_area.hide()
        self.editor_splitter.setStretchFactor(0, 3)
        self.editor_splitter.setStretchFactor(1, 2)
        self.h_head_layout.addWidget(self.editor_splitter, 4)

        self.v_settings_layout = QVBoxLayout()
        self.v_settings_layout.setSpacing(10)
        self.SettingsTab = SettingsTab()
        self.settings_page = QScrollArea()
        self.settings_page.setWidgetResizable(True)
        self.settings_page.setWidget(self.SettingsTab)
        self.page_stack.addWidget(self.settings_page)
        self.SettingsTab.black_list_menu.confirm_button.clicked.connect(
            lambda: self.bl_list_func()
        )

        self.GenButtons = GenButtons()
        sidebar_layout.addWidget(self.GenButtons)
        sidebar_layout.setStretch(0, 1)
        self.but = self.GenButtons.buttons()
        self.but[0].clicked.connect(self.replace_text)
        self.but[1].clicked.connect(self.text_division_result)
        self.but[1].setObjectName("PrimaryButton")
        self.navigation = QWidget()
        nav_layout = QHBoxLayout(self.navigation)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        self.nav_buttons = []
        for title, callback in (("Редактор", self.open_main_page),
                                ("Telegram", self.open_telegram_manager),
                                ("Настройки", lambda: self.show_settings(0)),
                                ("Журнал", lambda: self.show_settings(2))):
            button = QPushButton(title)
            button.setCheckable(True)
            button.clicked.connect(callback)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)
        nav_layout.addStretch()
        self.main_layout.insertWidget(1, self.navigation)

        self.TelegramManager = TelegramManagerWidget()
        self.TelegramManager.black_list_menu.confirm_button.clicked.connect(
            lambda: self.bl_list_func(self.TelegramManager.black_list_menu)
        )
        self.page_stack.addWidget(self.TelegramManager)
        self.compact_page = QWidget()
        self.compact_layout = QVBoxLayout(self.compact_page)
        self.compact_layout.setContentsMargins(4, 4, 4, 4)
        self.page_stack.addWidget(self.compact_page)
        self.compact = False
        self.full_page = self.main_page
        self.page_stack.currentChanged.connect(self.sync_navigation)
        self.SettingsTab.tab_widget.currentChanged.connect(self.sync_navigation)
        self.sync_navigation()
        self.motion_toggle.toggled.connect(self.update_border_motion)

        self.setup_telegram_controller()

    def update_border_motion(self, enabled):
        for border in self.findChildren(AnimatedBorder):
            border.set_animated(enabled)

    def change_theme(self):
        key = apply_theme(self.theme_picker.currentData())
        self.preferences.setValue("theme", key)
        self.preferences.sync()

    def show_settings(self, tab):
        self.SettingsTab.tab_widget.setCurrentIndex(tab)
        self.page_stack.setCurrentWidget(self.settings_page)
        self.sync_navigation()

    def sync_navigation(self):
        page = self.page_stack.currentWidget()
        index = 0 if page == self.main_page else 1 if page == self.TelegramManager else 3 if self.SettingsTab.tab_widget.currentIndex() == 2 else 2
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)

    def animate_widget(self, widget):
        if not self.motion_toggle.isChecked():
            return
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", widget)
        animation.setDuration(220)
        animation.setStartValue(0.25)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.finished.connect(lambda: widget.setGraphicsEffect(None))
        widget._appearance_animation = animation
        animation.start()

    def set_compact(self, enabled):
        if enabled == self.compact:
            return
        self.compact = enabled
        if enabled:
            self.full_page = self.page_stack.currentWidget()
            self.compact_layout.addWidget(self.ImageResult)
            self.ImageResult.set_compact(True)
            self.page_stack.setCurrentWidget(self.compact_page)
        else:
            self.sidebar.layout().insertWidget(0, self.ImageResult)
            self.ImageResult.set_compact(False)
            self.page_stack.setCurrentWidget(self.full_page)
        self.header.setVisible(not enabled)
        self.navigation.setVisible(not enabled)

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
        first_split = self.results_area.isHidden()
        self.results_area.show()
        if first_split:
            height = self.editor_splitter.height()
            self.editor_splitter.setSizes([int(height * .6), int(height * .4)])
        self.empty_results.hide()
        for result_box in self.findChildren(ResultWidget):
            result_box.setParent(None)
            result_box.deleteLater()

        for text_block in text_division(self.TextWidget.get_general_text()):
            result_box = ResultWidget()
            result_box.setMinimumWidth(280)
            result_box.border = AnimatedBorder(result_box.result_text, self.motion_toggle.isChecked())
            result_box.set_text(text_block)
            self.connect_result_to_telegram(result_box)
            self.v_text_result_layout.addWidget(result_box, 1)
            self.animate_widget(result_box)
