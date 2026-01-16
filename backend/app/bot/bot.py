# backend/app/bot/bot.py — инициализация Telegram-бота
# Назначение: ленивое создание бота, безопасно для тестов

from aiogram import Bot
from app.core.settings import settings

bot: Bot | None = None  # (я добавил)


def get_bot() -> Bot | None:
    """
    Возвращает экземпляр Telegram-бота.
    В тестах и при отсутствии токена возвращает None.
    """
    global bot

    if settings.testing:  # (я добавил)
        return None

    if not settings.telegram_api_token:  # (я добавил)
        return None

    if bot is None:
        bot = Bot(token=settings.telegram_api_token)

    return bot
