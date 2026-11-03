import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from texteditor.ui.main_window_widget import \
    MainWindowW
from texteditor.services.app_logger import \
    setup_logging
from texteditor.ui.themes import apply_theme, appearance_settings
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
        self.setMinimumSize(280, 245)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "widget"):
            # Hysteresis keeps the layout stable close to the compact boundary.
            compact = self.width() < 620 or self.height() < 420
            if self.widget.compact:
                compact = self.width() < 680 or self.height() < 460
            self.widget.set_compact(compact)


app = QApplication(sys.argv)
setup_logging()
apply_theme(appearance_settings().value("theme", "paper"))
window = MainWindow()
window.show()
sys.exit(app.exec())

