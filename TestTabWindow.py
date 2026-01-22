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
    QMenu
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

        self.h_layout = QHBoxLayout()
        self.v_enualayout = QVBoxLayout()
        self.v_textlayout = QVBoxLayout()
        self.v_settingslayout = QVBoxLayout()

        self.setLayout(self.h_layout)

        #self.v_settingslayout.addLayout(self.h_layout)

        self.h_layout.addLayout(self.v_enualayout, 2)
        self.h_layout.addLayout(self.v_textlayout, 4)
        self.h_layout.addLayout(self.v_settingslayout, 2)

        self.v_enualayout.addWidget(ImageResult())

        # self.TextBoxResult = ResultWidget()
        # self.TextBoxResult.box.setTitle('EN Text')
        # self.v_enualayout.addWidget(self.TextBoxResult)


        self.TextWidget = TextWidget()
        self.v_textlayout.addWidget(self.TextWidget)

        self.SettingsTab = SettingsTab()
        self.v_settingslayout.addWidget(self.SettingsTab)

        def bl_list_func():

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

        self.SettingsTab.confirm_button.clicked.connect(lambda : bl_list_func())

        self.GenButtons = GenButtons()
        self.v_settingslayout.addWidget(self.GenButtons)

        self.but = self.GenButtons.buttons()
        self.but[0].clicked.connect(lambda: self.replace_text())
        self.but[1].clicked.connect(lambda: self.text_division_result())

    def replace_text(self):
        self.TextWidget.set_general_text(Func.accept_black_list(self.TextWidget.get_general_text()))

    def get_text_widget(self):
        return self.TextWidget

    def text_division_result(self):
        for bx in self.findChildren(ResultWidget):
            bx.setParent(None)
            bx.deleteLater()
        for text_block in text_division(self.TextWidget.get_general_text()):
            result_box = ResultWidget()
            result_box.set_text(text_block)
            self.v_enualayout.addWidget(result_box)


class ResultWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resultText = ''
        self.text = ''
        self.box = QGroupBox(self.text)
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.h_layout = QHBoxLayout()

        self.enText = QTextEdit()
        self.copyButton = QPushButton("Copy")
        self.techButton = QPushButton("Tech")
        self.techButton2 = QPushButton("Tech2")

        self.techButton.setVisible(False)
        self.techButton2.setVisible(False)

        #Test
        self.enText.setText(self.resultText)

        self.v_layout.addWidget(self.enText)
        self.v_layout.addLayout(self.h_layout)
        self.h_layout.addWidget(self.copyButton)
        self.h_layout.addWidget(self.techButton)
        self.h_layout.addWidget(self.techButton2)

        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)

    def get_text(self):
        return self.enText.toPlainText()
    def set_text(self, text):
        self.enText.setPlainText(text)

    def get_copy_button(self):
        return self.copyButton

    def get_tech_button(self):
        return self.techButton

    def get_tech_button2(self):
        return self.techButton2



class TextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QGroupBox("General Text Editor")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.imageBox = QGroupBox("Image DropBox")
        self.imageLayout = QVBoxLayout(self.imageBox)

        self.image = QLabel()
        self.image.setMinimumHeight(150)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setText('Preview')
        self.imageLayout.addWidget(self.image)

        self.v_layout.addWidget(self.imageBox)

        self.GeneralText = QTextEdit()
        self.GeneralText.setAcceptRichText(False)
        self.text = self.GeneralText.toPlainText()
        self.v_layout.addWidget(self.GeneralText)


        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)

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

        self.imageresult = QLabel("preview")
        self.imageresult.setMinimumHeight(150)
        self.imageresult.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(self.imageresult)

        box_layout.addWidget(self.boxImage)

        controls = QHBoxLayout()
        self.combobox = QComboBox()
        self.combobox.addItems(["WebP", "PNG", "JPEG"])
        self.resButton = QPushButton("Result")

        controls.addWidget(self.combobox)
        controls.addWidget(self.resButton)
        box_layout.addLayout(controls)

        mainlayout = QVBoxLayout(self)
        mainlayout.addWidget(self.box)

    def set_image(self, pixmap):
        self.imageresult.setPixmap(pixmap)
    def get_image(self):
        return self.imageresult

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

        self.settings = QTextEdit()
        self.tabWidget.addTab(self.settings, "Settings")
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
