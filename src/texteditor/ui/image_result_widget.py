from PyQt6.QtCore import \
    Qt
from PyQt6.QtGui import \
    QDragEnterEvent, \
    QDropEvent, \
    QPixmap, \
    QDragLeaveEvent
from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QLabel, \
    QHBoxLayout, \
    QComboBox, \
    QPushButton

class ImageResult(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QGroupBox("Convert")
        box_layout = QVBoxLayout(self.box)

        self.boxImage = QGroupBox("Image result")
        image_layout = QVBoxLayout(self.boxImage)

        self.dropZone = DropZone()
        image_layout.addWidget(self.dropZone)
        # self.image_result = QLabel("preview")
        # self.image_result.setMinimumHeight(150)
        # self.image_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # image_layout.addWidget(self.image_result)

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


class DropZone(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Перетащи изображение сюда")
        self.setMinimumSize(240, 160)
        self.setStyleSheet("border: 2px dashed #888; padding: 20px;")

        self.setAcceptDrops(True)
    def dragEnterEvent(self, event: QDragEnterEvent):
        print("devent")
        md = event.mimeData()
        print(type(md))
        if md.hasUrls():
            for url in md.urls():
                path = url.toLocalFile().lower()
                if path.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        print("drevent")
        md = event.mimeData()
        if md.hasImage():
            img = md.imageData()
            pix = QPixmap.fromImage(img)
        else:
            path = md.urls()[0].toLocalFile()
            pix = QPixmap(path)
        self.setScaledContents(True)
        self.setPixmap(pix)
        event.acceptProposedAction()


