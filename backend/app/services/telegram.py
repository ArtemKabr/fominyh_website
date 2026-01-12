# app/services/telegram.py — отправка сообщений в Telegram

import httpx
from app.core.settings import settings


async def send_telegram_message(chat_id: str, text: str) -> None:
    """Отправить сообщение в Telegram."""  #

    if not settings.telegram_bot_token:
        return

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
            },
        )
