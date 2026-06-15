from texteditor.services.app_logger import get_logger
from texteditor.services.black_list import refresh_black_list
from texteditor.services.telegram import get_telegram_messages
from texteditor.ui.result_widget import ResultWidget
from texteditor.ui.telegram_workers import (
    TelegramAuthWorker,
    TelegramCheckWorker,
    TelegramMessageActionWorker,
    TelegramMessagesSyncWorker,
    TelegramSendWorker,
)


logger = get_logger(__name__)


class TelegramControllerMixin:
    def setup_telegram_controller(self):
        setting_menu = self.SettingsTab.setting_menu
        setting_menu.button_save.clicked.connect(
            self.check_telegram_connection
        )
        setting_menu.telegram_auth.send_code_button.clicked.connect(
            self.request_telegram_login_code
        )
        setting_menu.telegram_auth.sign_in_button.clicked.connect(
            self.complete_telegram_login
        )
        setting_menu.telegram_auth.qr_login_button.clicked.connect(
            self.start_telegram_qr_login
        )

        self.but[2].clicked.connect(self.open_telegram_manager)
        self.TelegramManager.back_requested.connect(self.open_main_page)
        self.TelegramManager.refresh_requested.connect(
            self.refresh_telegram_messages
        )
        self.TelegramManager.update_requested.connect(
            self.update_telegram_message
        )
        self.TelegramManager.delete_requested.connect(
            self.delete_telegram_message
        )

        self.telegram_workers = []
        self.telegram_action_workers = []
        self.telegram_check_worker = None
        self.telegram_messages_sync_worker = None
        self.telegram_auth_worker = None
        self.check_telegram_connection()

    def connect_result_to_telegram(self, result_box):
        result_box.push_to_telegram_requested.connect(self.push_to_telegram)

    def push_to_telegram(self, text):
        result_box = self.sender()
        credentials = self.telegram_credentials()
        if not self.telegram_api_configured(credentials):
            if isinstance(result_box, ResultWidget):
                result_box.set_telegram_status(
                    "idle",
                    "Configure and sign in to Telegram in Settings.",
                )
            return

        worker = TelegramSendWorker(
            credentials,
            text,
            self.ImageResult.get_current_image_path(),
            self,
        )
        worker.result_box = result_box
        self.telegram_workers.append(worker)
        worker.sent.connect(
            lambda records: self.telegram_send_finished(worker, records)
        )
        worker.failed.connect(
            lambda error: self.telegram_send_failed(worker, error)
        )
        worker.finished.connect(lambda: self.telegram_worker_finished(worker))
        worker.start()
        logger.info("Sending result block to Telegram")

    def telegram_send_finished(self, worker, records):
        logger.info("Result block sent to Telegram")
        if isinstance(worker.result_box, ResultWidget):
            worker.result_box.set_telegram_status("sent")
        if records:
            self.refresh_telegram_messages(sync=False)

    def telegram_send_failed(self, worker, error):
        logger.error("Telegram send failed: %s", error)
        if isinstance(worker.result_box, ResultWidget):
            worker.result_box.set_telegram_status("idle", error)

    def telegram_worker_finished(self, worker):
        self.telegram_workers.remove(worker)
        worker.deleteLater()

    def check_telegram_connection(self):
        credentials = self.telegram_credentials()
        if not self.telegram_api_configured(credentials):
            self.GenButtons.set_telegram_status("disconnected")
            return
        if self.telegram_check_worker and self.telegram_check_worker.isRunning():
            return

        self.GenButtons.set_telegram_status("checking")
        worker = TelegramCheckWorker(credentials, self)
        self.telegram_check_worker = worker
        worker.connected.connect(self.telegram_connection_succeeded)
        worker.failed.connect(self.telegram_connection_failed)
        worker.finished.connect(self.telegram_check_finished)
        worker.start()

    def telegram_connection_failed(self, error):
        logger.error("Telegram connection check failed: %s", error)
        self.GenButtons.set_telegram_status(
            "disconnected",
            "Telegram account: not signed in",
        )
        self.GenButtons.telegram_status.setToolTip(error)

    def telegram_connection_succeeded(self):
        self.GenButtons.set_telegram_status("connected")
        self.SettingsTab.setting_menu.set_telegram_auth_status(
            "Telegram account is connected.",
            True,
        )

    def telegram_check_finished(self):
        worker = self.telegram_check_worker
        self.telegram_check_worker = None
        worker.deleteLater()

    def open_telegram_manager(self):
        self.page_stack.setCurrentWidget(self.TelegramManager)
        self.refresh_telegram_messages()
        self.refresh_black_list_menu(self.TelegramManager.black_list_menu)

    def open_main_page(self):
        self.refresh_black_list_menu(self.SettingsTab.black_list_menu)
        self.page_stack.setCurrentWidget(self.main_page)

    @staticmethod
    def refresh_black_list_menu(menu):
        menu.clear_black_list()
        for item in refresh_black_list():
            menu.add_black_list_item(str(item))

    def refresh_telegram_messages(self, sync=True):
        credentials = self.telegram_credentials()
        if not self.telegram_api_configured(credentials):
            self.TelegramManager.set_messages([])
            self.TelegramManager.set_operation_result(
                "Telegram account is not configured.",
                False,
            )
            return
        if not sync:
            self.TelegramManager.set_messages(
                get_telegram_messages(credentials, 30)
            )
            return
        if (
            self.telegram_messages_sync_worker
            and self.telegram_messages_sync_worker.isRunning()
        ):
            return

        self.TelegramManager.set_busy(True, "Loading Telegram messages...")
        worker = TelegramMessagesSyncWorker(credentials, self)
        self.telegram_messages_sync_worker = worker
        worker.loaded.connect(self.telegram_messages_loaded)
        worker.failed.connect(self.telegram_messages_load_failed)
        worker.finished.connect(self.telegram_messages_sync_finished)
        worker.start()

    def telegram_messages_loaded(self, records):
        self.TelegramManager.set_messages(records)
        self.TelegramManager.set_operation_result(
            f"Loaded {len(records)} Saved Messages.",
            True,
        )

    def telegram_messages_load_failed(self, error):
        logger.error("Telegram messages sync failed: %s", error)
        credentials = self.telegram_credentials()
        self.TelegramManager.set_messages(
            get_telegram_messages(credentials, 30)
        )
        self.TelegramManager.set_operation_result(
            f"{error} Showing locally saved messages.",
            False,
        )

    def telegram_messages_sync_finished(self):
        worker = self.telegram_messages_sync_worker
        self.telegram_messages_sync_worker = None
        worker.deleteLater()

    def update_telegram_message(self, record_id, text):
        self.start_telegram_message_action("edit", record_id, text)

    def delete_telegram_message(self, record_id):
        self.TelegramManager.set_busy(True, "Deleting message...")
        self.start_telegram_message_action("delete", record_id)

    def start_telegram_message_action(self, action, record_id, text=""):
        credentials = self.telegram_credentials()
        if not self.telegram_api_configured(credentials):
            self.TelegramManager.set_operation_result(
                "Telegram account is not configured.",
                False,
            )
            return

        worker = TelegramMessageActionWorker(
            action,
            credentials,
            record_id,
            text,
            self,
        )
        self.telegram_action_workers.append(worker)
        worker.succeeded.connect(
            lambda message: self.telegram_message_action_succeeded(
                worker,
                message,
            )
        )
        worker.failed.connect(
            lambda error: self.telegram_message_action_failed(worker, error)
        )
        worker.finished.connect(
            lambda: self.telegram_message_action_finished(worker)
        )
        worker.start()

    def telegram_message_action_succeeded(self, worker, message):
        del worker
        self.refresh_telegram_messages(sync=False)
        self.TelegramManager.set_operation_result(message, True)

    def telegram_message_action_failed(self, worker, error):
        del worker
        logger.error("Telegram message operation failed: %s", error)
        self.TelegramManager.set_operation_result(error, False)

    def telegram_message_action_finished(self, worker):
        self.telegram_action_workers.remove(worker)
        worker.deleteLater()

    def telegram_credentials(self):
        return self.SettingsTab.setting_menu.get_telegram_credentials()

    def telegram_api_configured(self, credentials=None):
        credentials = credentials or self.telegram_credentials()
        return bool(credentials.get("api_id") and credentials.get("api_hash"))

    def request_telegram_login_code(self):
        self.start_telegram_auth("request_code")

    def complete_telegram_login(self):
        self.start_telegram_auth(
            "sign_in",
            self.SettingsTab.setting_menu.get_telegram_login_code(),
            self.SettingsTab.setting_menu.get_telegram_password(),
        )

    def start_telegram_qr_login(self):
        self.start_telegram_auth(
            "qr_login",
            password=self.SettingsTab.setting_menu.get_telegram_password(),
        )

    def start_telegram_auth(self, action, code="", password=""):
        if self.telegram_auth_worker and self.telegram_auth_worker.isRunning():
            return
        credentials = self.telegram_credentials()
        self.SettingsTab.setting_menu.set_telegram_auth_status(
            "Connecting to Telegram..."
        )
        worker = TelegramAuthWorker(
            action,
            credentials,
            code,
            password,
            self,
        )
        self.telegram_auth_worker = worker
        worker.succeeded.connect(self.telegram_auth_succeeded)
        worker.failed.connect(self.telegram_auth_failed)
        worker.qr_ready.connect(self.telegram_qr_ready)
        worker.code_sent.connect(
            self.SettingsTab.setting_menu.show_telegram_code_step
        )
        worker.password_required.connect(
            self.SettingsTab.setting_menu.show_telegram_password_step
        )
        worker.finished.connect(self.telegram_auth_finished)
        worker.start()

    def telegram_auth_succeeded(self, message):
        self.SettingsTab.setting_menu.reset_telegram_auth_steps()
        self.SettingsTab.setting_menu.set_telegram_auth_status(message, True)
        logger.info(message)
        if "already signed in" in message or "account signed in" in message:
            self.check_telegram_connection()

    def telegram_auth_failed(self, error):
        logger.error("Telegram authorization failed: %s", error)
        self.SettingsTab.setting_menu.set_telegram_auth_status(error)
        if "2FA password" in error:
            self.SettingsTab.setting_menu.set_telegram_auth_status(
                "Enter the Telegram cloud password and press Sign in."
            )
        self.GenButtons.set_telegram_status("disconnected")

    def telegram_qr_ready(self, image_bytes):
        self.SettingsTab.setting_menu.set_telegram_qr_code(image_bytes)
        self.SettingsTab.setting_menu.set_telegram_auth_status(
            "Scan the QR code in Telegram: Settings -> Devices -> "
            "Link Desktop Device."
        )

    def telegram_auth_finished(self):
        worker = self.telegram_auth_worker
        self.telegram_auth_worker = None
        worker.deleteLater()
