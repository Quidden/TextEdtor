import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from src.texteditor.ui.main_window_widget import \
    MainWindowW
from src.texteditor.services.app_logger import \
    setup_logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextEdtor")
        self.resize(1440, 820)
        self.widget = MainWindowW()
        self.setCentralWidget(self.widget)


app = QApplication(sys.argv)
setup_logging()
style_path = Path(__file__).parent / "texteditor" / "ui" / "app_style.qss"
if style_path.exists():
    style = style_path.read_text(encoding="utf-8")
    check_mark_path = (style_path.parent / "check_mark.svg").as_posix()
    app.setStyleSheet(style.replace("CHECK_MARK_ICON", check_mark_path))
window = MainWindow()
window.show()
sys.exit(app.exec())

