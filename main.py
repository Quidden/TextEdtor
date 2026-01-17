import sys

from PyQt6.QtCore import \
    Qt
import TestTabWindow
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QCheckBox
)

from TestTabWindow import \
    Program


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        #self.setGeometry(100, 100, 300, 200)
        self.widget = Program()
        self.setCentralWidget(self.widget)




app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
