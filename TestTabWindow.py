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
    QGroupBox
from PyQt6.uic.properties import \
    QtWidgets



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

        self.v_textlayout.addWidget(TextWidget())

        self.v_settingslayout.addWidget(SettingsTab())
        self.v_settingslayout.addWidget(GenButtons())


class ResultWidget(QWidget):
    def __init__(self):
        super().__init__()
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

        self.v_layout.addWidget(self.enText)
        self.v_layout.addLayout(self.h_layout)
        self.h_layout.addWidget(self.copyButton)
        self.h_layout.addWidget(self.techButton)
        self.h_layout.addWidget(self.techButton2)

        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)


class TextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QGroupBox("General Text Editor")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.imageBox = QGroupBox("Image DropBox")
        imageLayout = QVBoxLayout(self.imageBox)

        self.image = QLabel()
        self.image.setMinimumHeight(150)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setText('Preview')
        imageLayout.addWidget(self.image)

        self.v_layout.addWidget(self.imageBox)

        self.GeneralText = QTextEdit()
        self.v_layout.addWidget(self.GeneralText)


        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)



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


class ImageResult(QWidget):
    def __init__(self):
        super().__init__()

        # Внешняя рамка секции
        self.box = QGroupBox("Convert")
        box_layout = QVBoxLayout(self.box)

        # Внутренняя рамка только для картинки
        self.boxImage = QGroupBox("Image result")
        image_layout = QVBoxLayout(self.boxImage)

        self.imageresult = QLabel("preview")
        self.imageresult.setMinimumHeight(150)
        self.imageresult.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(self.imageresult)

        # Добавляем внутренний groupbox в внешний
        box_layout.addWidget(self.boxImage)

        # Панель управления (формат + кнопка)
        controls = QHBoxLayout()
        self.combobox = QComboBox()
        self.combobox.addItems(["WebP", "PNG", "JPEG"])
        self.resButton = QPushButton("Result")

        controls.addWidget(self.combobox)
        controls.addWidget(self.resButton)
        box_layout.addLayout(controls)

        # Layout для самого виджета ImageResult
        mainlayout = QVBoxLayout(self)
        mainlayout.addWidget(self.box)

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QGroupBox("Settings")
        self.v_layout = QVBoxLayout()
        self.box.setLayout(self.v_layout)

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(QTextEdit(), "Black list")
        self.tabWidget.addTab(QTextEdit(), "Settings")
        self.tabWidget.addTab(QTextEdit(), "Log")
        self.v_layout.addWidget(self.tabWidget)

        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.box)
