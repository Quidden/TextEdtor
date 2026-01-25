import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from src.ui.TestTabWindow import \
    MainWindowW


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        #self.setGeometry(100, 100, 300, 200)
        self.widget = MainWindowW()
        self.setCentralWidget(self.widget)




app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
