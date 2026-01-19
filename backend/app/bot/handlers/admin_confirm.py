# backend/app/bot/handlers/admin_confirm.py — обработка кнопок админа
# Назначение: подтверждение и отмена записей через Telegram

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.core.database import async_session_maker
from app.models.booking import Booking, BookingStatus
from app.models.user import User
# from app.tasks.notifications import send_booking_reminder

router = Router()


@router.callback_query(F.data.startswith("admin:confirm:"))
async def confirm_booking(callback: CallbackQuery) -> None:
    """Подтверждение записи администратором."""  # (я добавил)
    booking_id = int(callback.data.split(":")[-1])

    async with async_session_maker() as session:
        booking = await session.get(Booking, booking_id)

        if not booking:
            await callback.answer("Запись не найдена", show_alert=True)
            return

        if booking.status == BookingStatus.CONFIRMED.value:
            await callback.answer("Уже подтверждена")
            return

        booking.status = BookingStatus.CONFIRMED.value
        await session.commit()

        user = await session.get(User, booking.user_id)

    await callback.message.edit_text(
        f"✅ Запись #{booking_id} подтверждена"
    )

    if user and user.telegram_chat_id:
        await callback.bot.send_message(
            chat_id=user.telegram_chat_id,
            text="✅ Ваша запись подтверждена. Ждём вас!",
        )

    await callback.answer()


@router.callback_query(F.data.startswith("admin:cancel:"))
async def cancel_booking(callback: CallbackQuery) -> None:
    """Отмена записи администратором."""  # (я добавил)
    booking_id = int(callback.data.split(":")[-1])

    async with async_session_maker() as session:
        booking = await session.get(Booking, booking_id)

        if not booking:
            await callback.answer("Запись не найдена", show_alert=True)
            return

        booking.status = BookingStatus.CANCELED.value
        await session.commit()

        user = await session.get(User, booking.user_id)

    await callback.message.edit_text(
        f"❌ Запись #{booking_id} отменена"
    )

    if user and user.telegram_chat_id:
        await callback.bot.send_message(
            chat_id=user.telegram_chat_id,
            text="❌ Ваша запись отменена администратором.",
        )

    await callback.answer()
