# backend/app/bot/keyboards/user.py — клавиатуры пользователя Telegram
# Назначение: inline-меню для пользователя

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  # (я добавил)


def user_main_menu_kb() -> InlineKeyboardMarkup:
    """Главное меню пользователя."""  # (я добавил)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(  # (я добавил)
                    text="📅 Записаться",
                    callback_data="user:book",
                )
            ],
            [
                InlineKeyboardButton(  # (я добавил)
                    text="📖 Мои записи",
                    callback_data="user:my_bookings",
                )
            ],
        ]
    )
