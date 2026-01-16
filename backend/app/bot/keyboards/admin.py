# backend/app/bot/keyboards/admin.py — клавиатуры админа
# Назначение: кнопки управления записями

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_confirm_booking_kb(booking_id: int) -> InlineKeyboardMarkup:
    """Кнопки подтверждения записи."""  # (я добавил)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data=f"admin:confirm:{booking_id}",
                ),
            ]
        ]
    )
