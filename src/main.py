import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from texteditor.ui.main_window_widget import \
    MainWindowW
from texteditor.services.app_logger import \
    setup_logging
from texteditor import \
    __version__


def resource_path(*parts):
    bundle_root = getattr(sys, "_MEIPASS", None)
    candidates = []
    if bundle_root:
        candidates.append(Path(bundle_root).joinpath(*parts))
    candidates.append(Path(__file__).resolve().parent.joinpath(*parts))
    candidates.append(Path(__file__).resolve().parent / "src" / Path(*parts))

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"TextEdtor {__version__}")
        self.resize(1440, 820)
        self.widget = MainWindowW()
        self.setCentralWidget(self.widget)


app = QApplication(sys.argv)
setup_logging()
style_path = resource_path("texteditor", "ui", "app_style.qss")
if style_path.exists():
    style = style_path.read_text(encoding="utf-8")
    check_mark_path = (style_path.parent / "check_mark.svg").as_posix()
    app.setStyleSheet(style.replace("CHECK_MARK_ICON", check_mark_path))
window = MainWindow()
window.show()
sys.exit(app.exec())

