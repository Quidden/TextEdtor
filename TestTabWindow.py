import PyQt6
from PyQt6.QtCore import \
    Qt
from PyQt6.QtGui import \
    QPixmap
from PyQt6.QtWidgets import \
    QVBoxLayout, \
    QHBoxLayout, \
    QTextEdit, \
    QPushButton, \
    QWidget, \
    QLabel, \
    QTabWidget, \
    QComboBox, \
    QGroupBox, \
    QLineEdit, \
    QListView, \
    QListWidget, \
    QMessageBox, \
    QMenu, \
    QCheckBox
from PyQt6.uic.properties import \
    QtWidgets
import Func
from Func import \
    black_list_load, \
    get_black_list_items, \
    black_list_item_delete, \
    refresh_black_list, \
    text_division


class Program(QWidget):
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
        self.SettingsTab.confirm_button.clicked.connect(lambda : self.bl_list_func())
        self.GenButtons = GenButtons()
        self.v_settings_layout.addWidget(self.GenButtons)
        self.but = self.GenButtons.buttons()
        self.but[0].clicked.connect(lambda: self.replace_text()) #func for accept blacklist
        self.but[1].clicked.connect(lambda: self.text_division_result()) #func for split main text
        self.h_head_layout.addLayout(self.v_settings_layout, 2)

    def bl_list_func(self):

        if not black_list_load(
                black_list=self.SettingsTab.black_list_item.text(),
                white_list=self.SettingsTab.white_list_item.text()):
            self.msg_box = QMessageBox()
            self.setWindowTitle("Error")
            self.msg_box.setText("Replace")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            if self.msg_box.exec() == QMessageBox.StandardButton.Ok:
                return

        black_list_load(
            black_list=self.SettingsTab.black_list_item.text(),
            white_list=self.SettingsTab.white_list_item.text())
        self.SettingsTab.clear_black_list()
        for item in refresh_black_list():
            self.SettingsTab.add_black_list_item(str(item))

    def replace_text(self):
        self.TextWidget.set_general_text(Func.accept_black_list(
            self.TextWidget.get_general_text(),
            self.SettingsTab.get_check_box_text_settings(),
            self.SettingsTab.get_check_box_text_empty_settings()))

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

class TextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QGroupBox("General Text Editor")
        self.v_head_box_layout = QVBoxLayout()
        self.box.setLayout(self.v_head_box_layout)


        self.image_box = QGroupBox("Image DropBox")
        self.imageLayout = QVBoxLayout(self.image_box)
        self.v_head_box_layout.addWidget(self.image_box)


        self.image = QLabel()
        self.image.setMinimumHeight(150)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setText('Preview')
        self.imageLayout.addWidget(self.image)


        self.GeneralText = QTextEdit()
        self.GeneralText.setAcceptRichText(False)
        self.text = self.GeneralText.toPlainText()
        self.v_head_box_layout.addWidget(self.GeneralText)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.box)

    def get_general_text(self):
        return self.GeneralText.toPlainText()
    def set_general_text(self, text):
        self.GeneralText.setPlainText(text)

    def get_image(self):
        return self.image
    def set_image(self, pixmap):
        self.image.setPixmap(pixmap)

class GenButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QGroupBox("General Buttons")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.button1 = QPushButton("Accept black list")
        self.button2 = QPushButton("Button2")
        self.button3 = QPushButton("Button3")
        self.button4 = QPushButton("Button4")
        self.button5 = QPushButton("Button5")
        self.button6 = QPushButton("Button6")

        self.v_layout.addWidget(self.button1)
        self.v_layout.addWidget(self.button2)
        self.v_layout.addWidget(self.button3)
        self.v_layout.addWidget(self.button4)
        self.v_layout.addWidget(self.button5)
        self.v_layout.addWidget(self.button6)

        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)

    def buttons(self):
        return self.button1, self.button2, self.button3, self.button4, self.button5, self.button6

class ImageResult(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QGroupBox("Convert")
        box_layout = QVBoxLayout(self.box)

        self.boxImage = QGroupBox("Image result")
        image_layout = QVBoxLayout(self.boxImage)

        self.image_result = QLabel("preview")
        self.image_result.setMinimumHeight(150)
        self.image_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(self.image_result)

        box_layout.addWidget(self.boxImage)

        controls = QHBoxLayout()
        self.combobox = QComboBox()
        self.combobox.addItems(["WebP", "PNG", "JPEG"])
        self.resButton = QPushButton("Result")

        controls.addWidget(self.combobox)
        controls.addWidget(self.resButton)
        box_layout.addLayout(controls)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.box)

    def set_image(self, pixmap):
        self.image_result.setPixmap(pixmap)
    def get_image(self):
        return self.image_result

    def get_res_button(self):
        return self.resButton

    def get_combobox(self):
        return self.combobox

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QGroupBox("Settings")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.tabWidget = QTabWidget()
        #self.blackList = QTextEdit()
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
        #self.v2_layout.addLayout(self.v3_layout)
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

        self.tabWidget.addTab(self.v2_widget, "Black list")

        self.v_settings = QWidget()
        self.v_settings_layout = QVBoxLayout(self.v_settings)
        self.v_settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.check_box_text_settings = QCheckBox("Text settings")
        self.check_box_text_empty_settings = QCheckBox("Empty text settings")
        self.v_settings_layout.addWidget(self.check_box_text_settings)
        self.v_settings_layout.addWidget(self.check_box_text_empty_settings)
        self.tabWidget.addTab(self.v_settings, "Settings")
        self.log = QTextEdit()
        self.tabWidget.addTab(self.log, "Log")
        self.v_layout.addWidget(self.tabWidget)

        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)

    def open_menu(self, position):
        item = self.b_list.itemAt(position)

        menu = QMenu(self)

        delete = menu.addAction("Delete")
        action = menu.exec(self.b_list.mapToGlobal(position))
        if action == delete:
            black_list_item_delete(self.b_list.row(item))
            self.clear_black_list()
            for item in refresh_black_list():
                self.b_list.addItem(str(item))


    def get_check_box_text_settings(self):
        return self.check_box_text_settings.isChecked()
    def get_check_box_text_empty_settings(self):
        return self.check_box_text_empty_settings.isChecked()

    def get_tab_widget(self):
        return self.tabWidget
    def get_box(self):
        return self.box

    def get_black_list(self):
        return self.b_list
    def add_black_list_item(self, text):
        self.b_list.addItem(text)
    def clear_black_list(self):
        self.b_list.clear()

    def get_settings(self):
        return self.settings
    def set_settings(self, text):
        self.settings.setPlainText(text)

    def get_log(self):
        return self.log
    def set_log(self, text):
        self.log.setPlainText(text)

    def get_refresh_button(self):
        return self.refresh_button

    def get_black_list_item(self):
        return self.black_list_item
    def get_white_list_item(self):
        return self.white_list_item
    def get_confirm_button(self):
        return self.confirm_button
