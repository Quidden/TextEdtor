import \
    os
from gzip import \
    WRITE

import \
    fmt
from PyQt6.QtCore import \
    Qt, \
    QBuffer, \
    QIODevice
from PyQt6.QtGui import \
    QDragEnterEvent, \
    QDropEvent, \
    QPixmap, \
    QDragLeaveEvent, \
    QImage, \
    QImageReader
from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QLabel, \
    QHBoxLayout, \
    QComboBox, \
    QPushButton, \
    QApplication

from src.texteditor.config import \
    IMAGE_DIR
from src.texteditor.services.app_logger import \
    app_logger
from PIL import Image


class ImageResult(QWidget):
    def __init__(self):
        super().__init__()

        self.image_result = None
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
        self.combobox.currentTextChanged.connect(
            lambda text: app_logger.log(f"Image output format changed to {text}", source=__file__)
        )
        self.resButton = QPushButton("Result")
        self.pasteButton = QPushButton("Paste")
        self.pasteButton.clicked.connect(self.paste_image)
        self.resButton.clicked.connect(self.convert_image)


        controls.addWidget(self.combobox)
        controls.addWidget(self.resButton)
        controls.addWidget(self.pasteButton)
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

    def paste_image(self):
        print("paste")
        app = QApplication.instance()
        clipboard = app.clipboard()
        image = clipboard.image()
        if image.isNull():
            print("null")
            app_logger.log("Image paste failed: clipboard has no image", False, source=__file__)
            self.dropZone.setText("Скопируйте изображение!")
            return
        try:
            os.makedirs(IMAGE_DIR, exist_ok=True)
        except OSError:
            app_logger.log(
                "Image paste failed: image directory cannot be created",
                False,
                source=__file__)
            return "mkdir error"
        image.save(IMAGE_DIR + "/image.png")
        self.image_result = image
        self.dropZone.setPixmap(QPixmap.fromImage(self.image_result))
        app_logger.log("Image pasted from clipboard", source=__file__)

    def convert_image(self):
        print("convert1")
        if self.image_result is None:
            app_logger.log("Image convert failed: no image selected", False, source=__file__)
            return

        app = QApplication.instance()
        clipboard = app.clipboard()
        buffer = QBuffer()
        print("convert2")
        try:
            img = Image.open(IMAGE_DIR + "/image.png")
        except OSError as error:
            app_logger.log(f"Image convert failed: {error}", False, source=__file__)
            return
        if self.combobox.currentText() == "WebP":
            img.save(IMAGE_DIR + "/image.webp", 'WEBP', quality=100)
            print("webp")
        if self.combobox.currentText() == "PNG":
            img.save(IMAGE_DIR + "/image.png", 'PNG', quality=100)
            print("png")
        if self.combobox.currentText() == "JPEG":
            img.save(IMAGE_DIR + "/image.jpeg", 'JPEG', quality=100)
            print("jpeg")
        conv_image = QImage()
        conv_image.loadFromData(buffer.data())
        clipboard.setImage(conv_image)
        app_logger.log(f"Image converted to {self.combobox.currentText()}", source=__file__)
        print("done")


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
                    app_logger.log("Image drag accepted", source=__file__)
                    return
        app_logger.log("Image drag rejected", False, source=__file__)
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
        app_logger.log("Image dropped", source=__file__)





