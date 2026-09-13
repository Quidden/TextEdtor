import os
from datetime import datetime

from texteditor.config import (
    TELEGRAM_MESSAGES_FILE,
    TELEGRAM_STATE_FILE,
)
from texteditor.services.telegram.client import (
    run_telegram,
    with_authorized_client,
)
from texteditor.services.telegram.errors import TelegramError
from texteditor.services.telegram.storage import load_json, save_json


def daily_hashtag():
    return datetime.now().strftime("#%Y_%m_%d")


async def send_daily_hashtag_if_needed(client):
    state = load_json(TELEGRAM_STATE_FILE, {})
    hashtag = daily_hashtag()
    if state.get("saved_messages_hashtag") == hashtag:
        return
    await client.send_message("me", hashtag)
    state["saved_messages_hashtag"] = hashtag
    save_json(TELEGRAM_STATE_FILE, state)


def media_label(message):
    if message.photo:
        return "Photo"
    if message.video:
        return "Video"
    if message.voice:
        return "Voice message"
    if message.audio:
        return "Audio"
    if message.gif:
        return "Animation"
    if message.sticker:
        return "Sticker"
    if message.document:
        return "Document"
    if message.media:
        return "Media"
    return ""


def record_from_message(message):
    label = media_label(message)
    text = message.raw_text or ""
    if label and text:
        message_type = "caption"
    elif label:
        message_type = "media"
    else:
        message_type = "text"
    return {
        "record_id": str(message.id),
        "chat_id": "Saved Messages",
        "message_id": message.id,
        "message_type": message_type,
        "media_label": label,
        "text": text,
        "editable": message_type in ("text", "caption"),
        "direction": "outgoing",
        "created_at": (
            message.date.astimezone().isoformat(timespec="seconds")
            if message.date
            else ""
        ),
    }


def save_message_records(records):
    save_json(TELEGRAM_MESSAGES_FILE, records)


def get_telegram_messages(credentials, limit=30):
    del credentials
    records = load_json(TELEGRAM_MESSAGES_FILE, [])
    return records[:limit] if isinstance(records, list) else []


def sync_telegram_messages(credentials, limit=30):
    async def operation(client):
        messages = await client.get_messages("me", limit=limit)
        records = [record_from_message(message) for message in messages]
        save_message_records(records)
        return records

    return run_telegram(with_authorized_client(credentials, operation))


def send_to_telegram(credentials, text, image_path=None):
    async def operation(client):
        remaining_text = text.strip()
        has_image = bool(image_path and os.path.isfile(image_path))
        if not remaining_text and not has_image:
            raise TelegramError("There is no text or image to send.")

        await send_daily_hashtag_if_needed(client)
        sent_messages = []
        if has_image:
            caption = remaining_text if len(remaining_text) <= 1024 else ""
            sent_messages.append(
                await client.send_file("me", image_path, caption=caption)
            )
            if caption:
                remaining_text = ""

        while remaining_text:
            part = remaining_text[:4096]
            if len(remaining_text) > 4096:
                split_at = part.rfind("\n")
                if split_at > 0:
                    part = part[:split_at]
            sent_messages.append(await client.send_message("me", part))
            remaining_text = remaining_text[len(part):].lstrip("\n")

        records = [record_from_message(message) for message in sent_messages]
        existing = get_telegram_messages(credentials, 30)
        record_ids = {record["record_id"] for record in records}
        save_message_records(
            (records + [
                record for record in existing
                if record.get("record_id") not in record_ids
            ])[:30]
        )
        return records

    return run_telegram(with_authorized_client(credentials, operation))


def edit_telegram_message(credentials, record_id, text):
    text = text.strip()
    if not text:
        raise TelegramError("Message text cannot be empty.")

    async def operation(client):
        message_id = int(record_id)
        records = get_telegram_messages(credentials, 30)
        record = next(
            (item for item in records if item.get("record_id") == record_id),
            None,
        )
        if not record or not record.get("editable"):
            raise TelegramError("This message cannot be edited.")
        limit = 1024 if record.get("message_type") == "caption" else 4096
        if len(text) > limit:
            raise TelegramError(f"Message cannot exceed {limit} characters.")
        await client.edit_message("me", message_id, text)
        return True

    result = run_telegram(with_authorized_client(credentials, operation))
    sync_telegram_messages(credentials, 30)
    return result


def delete_telegram_message(credentials, record_id):
    async def operation(client):
        await client.delete_messages("me", [int(record_id)], revoke=True)
        return True

    result = run_telegram(with_authorized_client(credentials, operation))
    sync_telegram_messages(credentials, 30)
    return result
