import asyncio
import os

from telethon.errors import (
    AuthTokenExpiredError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
from telethon.tl import types

from texteditor.config import TELEGRAM_LOGIN_STATE_FILE
from texteditor.services.telegram.client import (
    create_client,
    run_telegram,
    validate_credentials,
    with_authorized_client,
)
from texteditor.services.telegram.errors import (
    TelegramError,
    TelegramPasswordRequired,
)
from texteditor.services.telegram.storage import load_json, save_json


_login_codes = {}


def request_login_code(credentials):
    async def operation():
        _, _, phone = validate_credentials(credentials, require_phone=True)
        client = create_client(credentials)
        await client.connect()
        try:
            if await client.is_user_authorized():
                return {
                    "status": "already_authorized",
                    "message": "Telegram account is already signed in.",
                }
            sent_code = await client.send_code_request(phone)
            _login_codes[phone] = sent_code.phone_code_hash
            save_json(
                TELEGRAM_LOGIN_STATE_FILE,
                {
                    "phone": phone,
                    "phone_code_hash": sent_code.phone_code_hash,
                },
            )
            return {
                "status": "code_sent",
                "message": sent_code_message(sent_code),
            }
        finally:
            await client.disconnect()

    return run_telegram(operation())


def complete_login(credentials, code, password=""):
    async def operation():
        _, _, phone = validate_credentials(credentials, require_phone=True)
        client = create_client(credentials)
        await client.connect()
        try:
            if await client.is_user_authorized():
                return True

            phone_code_hash = _login_codes.get(phone)
            if not phone_code_hash:
                login_state = load_json(TELEGRAM_LOGIN_STATE_FILE, {})
                if login_state.get("phone") == phone:
                    phone_code_hash = login_state.get("phone_code_hash")
            if not phone_code_hash:
                raise TelegramError("Request a login code first.")

            try:
                await client.sign_in(
                    phone=phone,
                    code=code.strip(),
                    phone_code_hash=phone_code_hash,
                )
            except SessionPasswordNeededError:
                if not password:
                    raise TelegramPasswordRequired(
                        "Two-step verification password is required."
                    )
                await client.sign_in(password=password)
            except PhoneCodeInvalidError as error:
                raise TelegramError("Telegram login code is invalid.") from error
            except PhoneCodeExpiredError as error:
                raise TelegramError(
                    "Telegram login code expired. Request a new code."
                ) from error
            except PasswordHashInvalidError as error:
                raise TelegramError(
                    "Two-step verification password is invalid."
                ) from error

            _login_codes.pop(phone, None)
            try:
                os.remove(TELEGRAM_LOGIN_STATE_FILE)
            except FileNotFoundError:
                pass
            return True
        finally:
            await client.disconnect()

    return run_telegram(operation())


def complete_password_login(credentials, password):
    if not password:
        raise TelegramPasswordRequired(
            "Enter the Telegram two-step verification password."
        )

    async def operation():
        client = create_client(credentials)
        await client.connect()
        try:
            if await client.is_user_authorized():
                return True
            try:
                await client.sign_in(password=password)
            except PasswordHashInvalidError as error:
                raise TelegramError(
                    "Two-step verification password is invalid."
                ) from error
            return True
        finally:
            await client.disconnect()

    return run_telegram(operation())


def login_with_qr(credentials, qr_callback, password=""):
    async def operation():
        client = create_client(credentials)
        await client.connect()
        try:
            if await client.is_user_authorized():
                return True
            qr_login = await client.qr_login()
            qr_callback(qr_login.url)
            try:
                await qr_login.wait(timeout=120)
            except SessionPasswordNeededError:
                if not password:
                    raise TelegramPasswordRequired(
                        "Enter the 2FA password, then press QR login again."
                    )
                await client.sign_in(password=password)
            except AuthTokenExpiredError as error:
                raise TelegramError(
                    "QR code expired. Press QR login to generate a new one."
                ) from error
            except asyncio.TimeoutError as error:
                raise TelegramError(
                    "QR login timed out. Press QR login to try again."
                ) from error
            return True
        finally:
            await client.disconnect()

    return run_telegram(operation())


def check_telegram_account(credentials):
    async def operation(client):
        me = await client.get_me()
        return {
            "id": me.id,
            "name": " ".join(
                part for part in (me.first_name, me.last_name) if part
            ),
        }

    return run_telegram(with_authorized_client(credentials, operation))


def sent_code_message(sent_code):
    code_type = sent_code.type
    delivery = "an active Telegram session"
    if isinstance(code_type, types.auth.SentCodeTypeSms):
        delivery = "SMS"
    elif isinstance(code_type, types.auth.SentCodeTypeCall):
        delivery = "a phone call"
    elif isinstance(code_type, types.auth.SentCodeTypeFlashCall):
        delivery = "a flash call"
    elif isinstance(code_type, types.auth.SentCodeTypeMissedCall):
        delivery = "a missed call"
    elif isinstance(code_type, types.auth.SentCodeTypeEmailCode):
        delivery = "email"
    elif isinstance(code_type, types.auth.SentCodeTypeFragmentSms):
        delivery = "Fragment SMS"
    elif isinstance(code_type, types.auth.SentCodeTypeFirebaseSms):
        delivery = "Firebase SMS"
    elif isinstance(code_type, types.auth.SentCodeTypeSmsPhrase):
        delivery = "SMS phrase"
    elif isinstance(code_type, types.auth.SentCodeTypeSmsWord):
        delivery = "SMS word"
    elif isinstance(code_type, types.auth.SentCodeTypeSetUpEmailRequired):
        delivery = "email setup"

    length = getattr(code_type, "length", None)
    timeout = getattr(sent_code, "timeout", None)
    details = f" Expected code length: {length}." if length else ""
    if timeout:
        details += f" Another delivery method may become available in {timeout}s."
    return f"Telegram accepted the request. Delivery: {delivery}.{details}"
