# backend/app/bot/bot.py — инициализация Telegram-бота

from aiogram import Bot, Dispatcher
from app.core.settings import settings

_bot: Bot | None = None
_dp: Dispatcher | None = None


def get_bot() -> Bot | None:
    """Вернуть Telegram-бота."""
    global _bot

    if settings.testing:
        return None

    if not settings.telegram_api_token:
        return None

    if _bot is None:
        _bot = Bot(token=settings.telegram_api_token)

    return _bot


def get_dispatcher() -> Dispatcher | None:
    """Вернуть Dispatcher."""
    global _dp

    if _dp is None:
        _dp = Dispatcher()

    return _dp
