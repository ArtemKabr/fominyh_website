# backend/app/bot/dispatcher.py — регистрация handlers
# Назначение: сбор всех router бота

from aiogram import Dispatcher

from app.bot.handlers.user_start import router as user_start_router
from app.bot.handlers.admin_confirm import router as admin_confirm_router
from app.bot.handlers.user_phone import router as user_phone_router
from app.bot.handlers.user_menu import router as user_menu_router  # (я добавил)
from app.bot.handlers.user_my_bookings import router as user_my_bookings_router


def setup_dispatcher(dp: Dispatcher) -> None:
    """Подключить все handlers."""  # (я добавил)

    dp.include_router(user_start_router)
    dp.include_router(admin_confirm_router)
    dp.include_router(user_phone_router)
    dp.include_router(user_menu_router)  # (я добавил)
    dp.include_router(user_my_bookings_router)  # (я добавил)
