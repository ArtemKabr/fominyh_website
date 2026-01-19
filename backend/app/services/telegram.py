# backend/app/services/telegram.py — отправка сообщений в Telegram
# Назначение: единая функция для celery и бота

from aiogram import Bot
from app.core.settings import settings

_bot: Bot | None = None


def get_bot() -> Bot:
    global _bot
    if _bot is None:
        _bot = Bot(token=settings.telegram_api_token)
    return _bot


async def send_telegram_message(chat_id: int, text: str) -> None:
    bot = get_bot()
    await bot.send_message(chat_id=chat_id, text=text)
