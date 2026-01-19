# backend/app/bot/handlers/__init__.py
# Назначение: экспорт роутеров Telegram-бота

from . import user_start  # (я добавил)
from . import user_phone  # (я добавил)
from . import admin_confirm  # (я добавил)

__all__ = [
    "user_start",
    "user_phone",
    "admin_confirm",
]  # (я добавил)
