# backend/app/bot/keyboards/booking.py — клавиатуры записи
# Назначение: inline-кнопки для бронирования

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # (я добавил)
from datetime import date, timedelta  # (я добавил)


def services_kb(services: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"book:svc:{sid}")]
            for sid, name in services
        ]
    )


def dates_kb(days: int = 7) -> InlineKeyboardMarkup:
    today = date.today()
    rows = []
    for i in range(days):
        d = today + timedelta(days=i)
        rows.append([
            InlineKeyboardButton(
                text=d.strftime("%d.%m"),
                callback_data=f"book:date:{d.isoformat()}",
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def slots_kb(slots: list[tuple[str, int]]) -> InlineKeyboardMarkup:
    # slots: [(HH:MM, slot_id)]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"book:slot:{sid}")]
            for label, sid in slots
        ]
    )
