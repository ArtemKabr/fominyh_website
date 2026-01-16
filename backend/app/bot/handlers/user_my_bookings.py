# backend/app/bot/handlers/user_my_bookings.py — мои записи
# Назначение: показать пользователю список его записей

from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.user import User
from app.models.booking import Booking
from app.models.service import Service
from app.bot.keyboards.user import user_main_menu_kb

router = Router()


def _fmt_dt(dt: datetime) -> str:
    """Формат даты/времени для Telegram."""  # (я добавил)
    return dt.strftime("%d.%m.%Y %H:%M")


@router.callback_query(F.data == "user:my_bookings")
async def my_bookings(callback: CallbackQuery) -> None:
    """Показать записи пользователя по telegram_chat_id."""  # (я добавил)

    telegram_chat_id = callback.from_user.id

    async with async_session_maker() as session:
        user = await session.scalar(
            select(User).where(User.telegram_chat_id == telegram_chat_id)
        )

        if not user:
            text = "Пользователь не найден. Нажмите /start."
            if callback.message.text != text:  # (я добавил)
                await callback.message.edit_text(text)
            await callback.answer()
            return

        rows = (
            await session.execute(
                select(Booking, Service)
                .join(Service, Service.id == Booking.service_id)
                .where(Booking.user_id == user.id)
                .order_by(Booking.start_time.desc())  # (я исправил)
                .limit(20)
            )
        ).all()

    if not rows:
        text = "📖 У вас пока нет записей."
        if callback.message.text != text:  # (я добавил)
            await callback.message.edit_text(
                text,
                reply_markup=user_main_menu_kb(),
            )
        await callback.answer()
        return

    lines: list[str] = ["📖 Ваши записи (последние 20):\n"]
    for booking, service in rows:
        lines.append(
            f"• #{booking.id} — {_fmt_dt(booking.start_time)} — "
            f"{service.name} — {booking.status}"
        )

    text = "\n".join(lines)

    if callback.message.text != text:  # (я добавил)
        await callback.message.edit_text(
            text,
            reply_markup=user_main_menu_kb(),
        )

    await callback.answer()
