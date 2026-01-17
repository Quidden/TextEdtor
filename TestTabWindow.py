import PyQt6
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
    QComboBox
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

        self.v_enualayout.addWidget(PuctureResult())
        self.v_enualayout.addWidget(ResultWidget())
        self.v_enualayout.addWidget(ResultWidget())

        self.v_textlayout.addWidget(TextWidget())

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(QTextEdit(), "Black list")
        self.tabWidget.addTab(QTextEdit(), "Settings")
        self.tabWidget.addTab(QTextEdit(), "Log")
        self.v_settingslayout.addWidget(self.tabWidget)
        self.v_settingslayout.addWidget(GenButtons())


class ResultWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.setLayout(self.v_layout)

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


class TextWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        self.Pict = QLabel()
        self.Pict.setMinimumHeight(200)
        self.v_layout.addWidget(self.Pict)

        self.GeneralText = QTextEdit()
        self.v_layout.addWidget(self.GeneralText)



class GenButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

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


class PuctureResult(QWidget):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        self.pictresult = QLabel()
        self.pictresult.setMinimumHeight(150)
        self.v_layout.addWidget(self.pictresult)

        self.h_layout = QHBoxLayout()

        self.combobox = QComboBox()
        self.combobox.addItems(["WebP", "PNG", "JPEG"])

        self.resButton = QPushButton("Result")

        self.h_layout.addWidget(self.combobox)
        self.h_layout.addWidget(self.resButton)
        self.v_layout.addLayout(self.h_layout)