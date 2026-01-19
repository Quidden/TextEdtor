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
    QLineEdit
from PyQt6.uic.properties import \
    QtWidgets
import Func



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
        self.TextBoxResult1 = ResultWidget()
        self.TextBoxResult1.box.setTitle('EN Text')
        self.TextBoxResult2 = ResultWidget()
        self.TextBoxResult2.box.setTitle('UKR Text')
        self.v_enualayout.addWidget(self.TextBoxResult1)
        self.v_enualayout.addWidget(self.TextBoxResult2)

        self.TextWidget = TextWidget()
        self.v_textlayout.addWidget(self.TextWidget)

        self.SettingsTab = SettingsTab()
        self.v_settingslayout.addWidget(self.SettingsTab)

        self.GenButtons = GenButtons()
        self.v_settingslayout.addWidget(self.GenButtons)

        self.but = self.GenButtons.buttons()
        self.but[0].clicked.connect(lambda: Func.test(self))



    def get_text_widget(self):
        return self.TextWidget

    def get_text_box_result1(self):
        return self.TextBoxResult1

    def get_text_box_result2(self):
        return self.TextBoxResult2



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

        self.button1 = QPushButton("Button1")
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
        self.blackList = QTextEdit()
        self.refresh_button = QPushButton("Refresh")
        self.delete_item = QPushButton("Delete")
        self.h_button_layout = QHBoxLayout()
        self.h_button_layout.addWidget(self.refresh_button)
        self.h_button_layout.addWidget(self.delete_item)

        self.v2_widget = QWidget()
        self.v2_layout = QVBoxLayout(self.v2_widget)
        self.v2_layout.addWidget(self.blackList)
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

    def get_tab_widget(self):
        return self.tabWidget
    def get_box(self):
        return self.box

    def get_black_list(self):
        return self.blackList
    def set_black_list(self, text):
        self.blackList.setPlainText(text)

    def get_settings(self):
        return self.settings
    def set_settings(self, text):
        self.settings.setPlainText(text)

    def get_log(self):
        return self.log
    def set_log(self, text):
        self.log.setPlainText(text)

