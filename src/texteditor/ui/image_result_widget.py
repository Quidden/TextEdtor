import os

from PyQt6.QtCore import (
    QMimeData,
    QPoint,
    Qt,
    QUrl,
)
from PyQt6.QtGui import (
    QDrag,
    QDragEnterEvent,
    QDropEvent,
    QImage,
    QMouseEvent,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from texteditor.config import IMAGE_DIR
from texteditor.services.app_logger import get_logger


logger = get_logger(__name__)


class ImageResult(QWidget):
    def __init__(self):
        super().__init__()

        self.image_result = None
        self.source_image_path = None
        self.output_image_path = None

        self.box = QGroupBox("Convert")
        box_layout = QVBoxLayout(self.box)
        box_layout.setSpacing(10)

        self.boxImage = QGroupBox("Image result")
        image_layout = QVBoxLayout(self.boxImage)

        self.dropZone = DropZone(self)
        image_layout.addWidget(self.dropZone)
        box_layout.addWidget(self.boxImage)

        controls = QHBoxLayout()
        controls.setSpacing(8)

        self.combobox = QComboBox()
        self.combobox.addItems(["WebP", "PNG", "JPEG"])

        self.resButton = QPushButton("Convert")
        self.pasteButton = QPushButton("Paste")
        self.pasteButton.clicked.connect(self.paste_image)
        self.resButton.clicked.connect(self.convert_image)

        controls.addWidget(self.combobox)
        controls.addWidget(self.resButton)
        controls.addWidget(self.pasteButton)
        box_layout.addLayout(controls)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.box)

    def _ensure_image_dir(self):
        os.makedirs(IMAGE_DIR, exist_ok=True)

    def _set_preview(self, image, drag_file_path=None):
        self.image_result = image
        self.dropZone.set_image(QPixmap.fromImage(image), drag_file_path)

    def _save_source_image(self, image, file_name="image.png"):
        self._ensure_image_dir()
        path = os.path.join(IMAGE_DIR, file_name)
        if not image.save(path):
            self.dropZone.setText("Could not save image")
            logger.error("Could not save source image to %s", path)
            return

        self.source_image_path = path
        self.output_image_path = None
        self._set_preview(image)
        logger.info("Source image saved: %s", path)

    def load_file(self, path):
        image = QImage(path)
        if image.isNull():
            self.dropZone.setText("Unsupported image")
            logger.warning("Unsupported image dropped: %s", path)
            return

        self.source_image_path = path
        self.output_image_path = None
        self._set_preview(image)
        logger.info("Image loaded: %s", path)

    def set_image(self, pixmap):
        self.dropZone.set_image(pixmap, self.output_image_path)

    def get_image(self):
        return self.dropZone

    def get_res_button(self):
        return self.resButton

    def get_combobox(self):
        return self.combobox

    def paste_image(self):
        image = QApplication.instance().clipboard().image()
        if image.isNull():
            self.dropZone.setText("Copy an image first")
            logger.warning("Paste image requested, but clipboard has no image")
            return

        self._save_source_image(image)

    def convert_image(self):
        if not self.source_image_path:
            self.dropZone.setText("Drop or paste an image first")
            logger.warning("Convert requested without source image")
            return

        image = QImage(self.source_image_path)
        if image.isNull():
            self.dropZone.setText("Could not read image")
            logger.error("Could not read source image: %s", self.source_image_path)
            return

        file_name, image_format = {
            "WebP": ("image.webp", "WEBP"),
            "PNG": ("image.png", "PNG"),
            "JPEG": ("image.jpeg", "JPEG"),
        }[self.combobox.currentText()]

        self._ensure_image_dir()
        output_path = os.path.join(IMAGE_DIR, file_name)

        if image_format == "JPEG":
            image = image.convertToFormat(QImage.Format.Format_RGB888)

        if not image.save(output_path, image_format, 100):
            self.dropZone.setText("Could not convert image")
            logger.error("Could not convert image to %s", output_path)
            return

        self.output_image_path = output_path
        QApplication.instance().clipboard().setImage(image)
        self._set_preview(image, output_path)
        logger.info("Image converted to %s: %s", image_format, output_path)


class DropZone(QLabel):
    def __init__(self, image_result, parent=None):
        super().__init__(parent)

        self.image_result = image_result
        self.drag_start_position = QPoint()
        self.drag_file_path = None
        self.preview_pixmap = QPixmap()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Drop image here")
        self.setMinimumSize(240, 160)
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)

    def set_image(self, pixmap, drag_file_path):
        self.preview_pixmap = pixmap
        self.drag_file_path = drag_file_path
        self._refresh_preview()

        if drag_file_path:
            self.setToolTip("Drag the converted file from here")
        else:
            self.setToolTip("Convert the image, then drag the result from here")

    def _refresh_preview(self):
        if self.preview_pixmap.isNull():
            return

        self.setPixmap(
            self.preview_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def resizeEvent(self, event):
        self._refresh_preview()
        super().resizeEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        md = event.mimeData()
        if md.hasImage():
            event.acceptProposedAction()
            return

        if md.hasUrls():
            for url in md.urls():
                path = url.toLocalFile().lower()
                if path.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    event.acceptProposedAction()
                    return

        event.ignore()

    def dropEvent(self, event: QDropEvent):
        md = event.mimeData()
        if md.hasImage():
            image = md.imageData()
            if isinstance(image, QImage):
                self.image_result._save_source_image(image)
        elif md.hasUrls():
            self.image_result.load_file(md.urls()[0].toLocalFile())

        event.acceptProposedAction()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not event.buttons() & Qt.MouseButton.LeftButton:
            return
        if not self.drag_file_path or not os.path.exists(self.drag_file_path):
            return

        distance = (event.position().toPoint() - self.drag_start_position).manhattanLength()
        if distance < QApplication.startDragDistance():
            return

        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(self.drag_file_path)])

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap())
        drag.exec(Qt.DropAction.CopyAction)
