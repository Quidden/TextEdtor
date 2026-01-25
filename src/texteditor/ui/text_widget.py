from PyQt6.QtCore import \
    Qt
from PyQt6.QtWidgets import \
    QWidget, \
    QGroupBox, \
    QVBoxLayout, \
    QLabel, \
    QTextEdit


class TextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QGroupBox("General Text Editor")
        self.v_head_box_layout = QVBoxLayout()
        self.box.setLayout(self.v_head_box_layout)


        # self.image_box = QGroupBox("Image DropBox")
        # self.imageLayout = QVBoxLayout(self.image_box)
        # self.v_head_box_layout.addWidget(self.image_box)


        self.image = QLabel()
        self.image.setMinimumHeight(150)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setText('Preview')
        # self.imageLayout.addWidget(self.image)


        self.GeneralText = QTextEdit()
        self.GeneralText.setAcceptRichText(False)
        self.text = self.GeneralText.toPlainText()
        self.v_head_box_layout.addWidget(self.GeneralText)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.box)

    def get_general_text(self):
        return self.GeneralText.toPlainText()
    def set_general_text(self, text):
        self.GeneralText.setPlainText(text)

    def get_image(self):
        return self.image
    def set_image(self, pixmap):
        self.image.setPixmap(pixmap)
