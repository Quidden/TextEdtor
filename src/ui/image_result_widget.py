from PyQt6.QtCore import \
    Qt
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

        self.image_result = QLabel("preview")
        self.image_result.setMinimumHeight(150)
        self.image_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(self.image_result)

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