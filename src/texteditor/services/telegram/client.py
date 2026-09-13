import asyncio
import os
import threading

from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    FloodWaitError,
    PhoneNumberInvalidError,
)

from texteditor.config import DATA_DIR, TELEGRAM_SESSION_FILE
from texteditor.services.telegram.errors import TelegramError


_client_lock = threading.Lock()


def validate_credentials(credentials, require_phone=False):
    try:
        api_id = int(str(credentials.get("api_id", "")).strip())
    except (TypeError, ValueError) as error:
        raise TelegramError("Telegram API ID must be a number.") from error

    api_hash = str(credentials.get("api_hash", "")).strip()
    phone = str(credentials.get("phone", "")).strip()
    if not api_hash:
        raise TelegramError("Telegram API hash is not configured.")
    if require_phone and not phone:
        raise TelegramError("Telegram phone number is not configured.")
    return api_id, api_hash, phone


def create_client(credentials):
    api_id, api_hash, _ = validate_credentials(credentials)
    os.makedirs(DATA_DIR, exist_ok=True)
    return TelegramClient(
        TELEGRAM_SESSION_FILE,
        api_id,
        api_hash,
        receive_updates=False,
    )


def run_telegram(coroutine):
    with _client_lock:
        try:
            return asyncio.run(coroutine)
        except TelegramError:
            raise
        except FloodWaitError as error:
            raise TelegramError(
                f"Telegram rate limit. Try again in {error.seconds} seconds."
            ) from error
        except ApiIdInvalidError as error:
            raise TelegramError("Telegram API ID or API hash is invalid.") from error
        except PhoneNumberInvalidError as error:
            raise TelegramError("Telegram phone number is invalid.") from error
        except Exception as error:
            raise TelegramError(str(error) or "Telegram operation failed.") from error


async def with_authorized_client(credentials, operation):
    client = create_client(credentials)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise TelegramError("Telegram account is not signed in.")
        return await operation(client)
    finally:
        await client.disconnect()
