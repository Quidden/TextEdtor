from PyQt6.QtWidgets import \
    QVBoxLayout, \
    QHBoxLayout, \
    QWidget, \
    QMessageBox
from src.texteditor.services.black_list import \
    black_list_load, \
    refresh_black_list, \
    accept_black_list
from src.texteditor.services.text_edit import \
    text_division
from src.texteditor.ui.get_button_widget import \
    GenButtons
from src.texteditor.ui.image_result_widget import \
    ImageResult
from src.texteditor.ui.result_widget import \
    ResultWidget
from src.texteditor.ui.setting_widget import \
    SettingsTab
from src.texteditor.ui.text_widget import \
    TextWidget


class MainWindowW(QWidget):
    def __init__(self):
        super().__init__()

        #Head layout to which other layouts are attached
        self.h_head_layout = QHBoxLayout()
        self.setLayout(self.h_head_layout)

        #The resulting layout with split text and image conversion settings
        self.v_text_result_layout = QVBoxLayout()
        self.v_text_result_layout.addWidget(ImageResult())
        self.h_head_layout.addLayout(self.v_text_result_layout, 2)

        #The main user text layout
        self.main_text = QVBoxLayout()
        self.TextWidget = TextWidget()
        self.main_text.addWidget(self.TextWidget)
        self.h_head_layout.addLayout(self.main_text, 4)

        #Settings layout includes a custom button widget
        self.v_settings_layout = QVBoxLayout()
        self.SettingsTab = SettingsTab()
        self.v_settings_layout.addWidget(self.SettingsTab)
        self.SettingsTab.black_list_menu.confirm_button.clicked.connect(lambda : self.bl_list_func())
        self.GenButtons = GenButtons()
        self.v_settings_layout.addWidget(self.GenButtons)
        self.but = self.GenButtons.buttons()
        self.but[0].clicked.connect(lambda: self.replace_text()) #func for accept blacklist
        self.but[1].clicked.connect(lambda: self.text_division_result()) #func for split main text
        self.h_head_layout.addLayout(self.v_settings_layout, 2)

    def bl_list_func(self):

        if not black_list_load(
                black_list=self.SettingsTab.black_list_menu.black_list_item.text(),
                white_list=self.SettingsTab.black_list_menu.white_list_item.text()):
            self.msg_box = QMessageBox()
            self.setWindowTitle("Error")
            self.msg_box.setText("Replace")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            if self.msg_box.exec() == QMessageBox.StandardButton.Ok:
                return

        black_list_load(
            black_list=self.SettingsTab.black_list_menu.black_list_item.text(),
            white_list=self.SettingsTab.black_list_menu.white_list_item.text())
        self.SettingsTab.black_list_menu.clear_black_list()
        for item in refresh_black_list():
            self.SettingsTab.black_list_menu.add_black_list_item(str(item))

    def replace_text(self):
        self.TextWidget.set_general_text(
            accept_black_list(
            self.TextWidget.get_general_text(),
            self.SettingsTab.setting_menu.get_check_box_text_settings(),
            self.SettingsTab.setting_menu.get_check_box_text_empty_settings()))

    def get_text_widget(self):
        return self.TextWidget
    def text_division_result(self):
        for bx in self.findChildren(ResultWidget):
            bx.setParent(None)
            bx.deleteLater()
        for text_block in text_division(self.TextWidget.get_general_text()):
            result_box = ResultWidget()
            result_box.set_text(text_block)
            self.v_text_result_layout.addWidget(result_box)


