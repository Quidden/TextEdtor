from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStyle,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from texteditor.ui.setting_tabs.black_list_menu_widget import BlackListMenu


class MessageRowWidget(QWidget):
    delete_requested = pyqtSignal(str)

    def __init__(self, record, parent=None):
        super().__init__(parent)
        self.record = record
        self.preview_lines = self._preview_lines(record)

        row_layout = QHBoxLayout(self)
        row_layout.setContentsMargins(6, 5, 6, 5)
        row_layout.setSpacing(8)

        self.label = QLabel()
        self.label.setMinimumWidth(0)
        row_layout.addWidget(self.label, 1)

        delete_button = QPushButton()
        delete_button.setObjectName("DeleteIconButton")
        delete_button.setToolTip("Delete message from Telegram")
        delete_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)
        )
        delete_button.setFixedSize(32, 32)
        delete_button.clicked.connect(
            lambda: self.delete_requested.emit(record["record_id"])
        )
        row_layout.addWidget(delete_button)
        self._update_preview()

    def _preview_lines(self, record):
        text = record.get("text", "").strip()
        media_label = record.get("media_label", "")
        if media_label:
            lines = [f"[{media_label}]"]
            lines.extend(text.splitlines()[:2])
        else:
            lines = text.splitlines()[:2] if text else ["(empty message)"]
        return [f"ID: {record.get('message_id')} | Saved", *lines]

    def _update_preview(self):
        available_width = max(80, self.width() - 58)
        metrics = self.label.fontMetrics()
        visible_lines = [
            metrics.elidedText(
                line,
                Qt.TextElideMode.ElideRight,
                available_width,
            )
            for line in self.preview_lines
        ]
        self.label.setText("\n".join(visible_lines))

    def resizeEvent(self, event):
        self._update_preview()
        super().resizeEvent(event)


class TelegramManagerWidget(QWidget):
    back_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    update_requested = pyqtSignal(str, str)
    delete_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_record = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        header_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_requested.emit)
        self.title = QLabel("Saved Messages manager")
        self.title.setObjectName("PageTitle")
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
        header_layout.addWidget(self.back_button)
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)
        main_layout.addLayout(content_layout, 1)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        content_layout.addLayout(left_layout, 3)

        messages_box = QGroupBox("Last 30 Saved Messages")
        messages_layout = QVBoxLayout(messages_box)
        self.messages_list = QListWidget()
        self.messages_list.currentItemChanged.connect(self.show_selected_message)
        messages_layout.addWidget(self.messages_list)
        left_layout.addWidget(messages_box, 3)

        black_list_box = QGroupBox("Black list")
        black_list_layout = QVBoxLayout(black_list_box)
        self.black_list_menu = BlackListMenu()
        black_list_layout.addWidget(self.black_list_menu)
        left_layout.addWidget(black_list_box, 2)

        editor_box = QGroupBox("Message editor")
        editor_layout = QVBoxLayout(editor_box)
        self.message_info = QLabel("Select a message from the list")
        self.message_info.setObjectName("StatusText")
        self.message_editor = QTextEdit()
        self.message_editor.setAcceptRichText(False)
        self.message_editor.setEnabled(False)
        self.update_button = QPushButton("Update in TG")
        self.update_button.setEnabled(False)
        self.update_button.clicked.connect(self.request_update)
        self.operation_status = QLabel("")
        self.operation_status.setObjectName("StatusText")
        self.operation_status.setWordWrap(True)
        editor_layout.addWidget(self.message_info)
        editor_layout.addWidget(self.message_editor, 1)
        editor_layout.addWidget(self.update_button)
        editor_layout.addWidget(self.operation_status)
        content_layout.addWidget(editor_box, 5)

    def set_messages(self, records):
        selected_id = (
            self.current_record.get("record_id")
            if self.current_record
            else None
        )
        self.messages_list.clear()
        selected_item = None

        for record in records:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, record)
            row = self._create_message_row(record)
            item.setSizeHint(row.sizeHint())
            self.messages_list.addItem(item)
            self.messages_list.setItemWidget(item, row)
            if record.get("record_id") == selected_id:
                selected_item = item

        if selected_item:
            self.messages_list.setCurrentItem(selected_item)
        elif self.messages_list.count():
            self.messages_list.setCurrentRow(0)
        else:
            self.clear_editor()

    def _create_message_row(self, record):
        row = MessageRowWidget(record)
        row.delete_requested.connect(self.delete_requested.emit)
        return row

    def show_selected_message(self, current, previous=None):
        del previous
        if not current:
            self.clear_editor()
            return

        self.current_record = current.data(Qt.ItemDataRole.UserRole)
        self.message_info.setText(
            "Message ID: {message_id} | Chat ID: {chat_id} | Type: {message_type}".format(
                **self.current_record
            )
        )
        self.message_editor.setPlainText(self.current_record.get("text", ""))
        self.message_editor.setEnabled(True)
        self.update_button.setEnabled(
            bool(self.current_record.get("editable", True))
        )
        if not self.current_record.get("editable", True):
            self.message_editor.setReadOnly(True)
            self.update_button.setToolTip(
                "The bot can edit only its own text messages and captions."
            )
        else:
            self.message_editor.setReadOnly(False)
            self.update_button.setToolTip("")
        self.operation_status.clear()

    def request_update(self):
        if not self.current_record:
            return
        self.set_busy(True, "Updating message...")
        self.update_requested.emit(
            self.current_record["record_id"],
            self.message_editor.toPlainText(),
        )

    def clear_editor(self):
        self.current_record = None
        self.message_info.setText("Select a message from the list")
        self.message_editor.clear()
        self.message_editor.setReadOnly(False)
        self.message_editor.setEnabled(False)
        self.update_button.setEnabled(False)

    def set_busy(self, busy, message=""):
        self.refresh_button.setEnabled(not busy)
        self.update_button.setEnabled(
            not busy
            and self.current_record is not None
            and bool(self.current_record.get("editable", True))
        )
        self.messages_list.setEnabled(not busy)
        if message:
            self.operation_status.setText(message)

    def set_operation_result(self, message, success):
        color = "#35c759" if success else "#ff5f57"
        self.operation_status.setStyleSheet(f"color: {color};")
        self.operation_status.setText(message)
        self.set_busy(False)
