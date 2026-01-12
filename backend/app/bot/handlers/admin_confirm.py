# backend/app/bot/handlers/admin_confirm.py
# Назначение: кнопки админа для управления записью

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.core.database import async_session_maker
from app.models.booking import Booking, BookingStatus
from app.models.user import User

router = Router()


@router.callback_query(F.data.startswith("confirm_booking:"))
async def confirm_booking(callback: CallbackQuery) -> None:
    booking_id = int(callback.data.split(":")[1])

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

    await callback.message.edit_text(f"✅ Запись #{booking_id} подтверждена")

    if user and user.telegram_chat_id:
        await callback.bot.send_message(  # ← ВАЖНО
            chat_id=user.telegram_chat_id,
            text="✅ Ваша запись подтверждена. Ждём вас!",
        )


@router.callback_query(F.data.startswith("cancel_booking:"))
async def cancel_booking(callback: CallbackQuery) -> None:
    booking_id = int(callback.data.split(":")[1])

    async with async_session_maker() as session:
        booking = await session.get(Booking, booking_id)

        if not booking:
            await callback.answer("Запись не найдена", show_alert=True)
            return

        booking.status = BookingStatus.CANCELED.value
        await session.commit()

        user = await session.get(User, booking.user_id)

    await callback.message.edit_text(f"❌ Запись #{booking_id} отменена")

    if user and user.telegram_chat_id:
        await callback.bot.send_message(  # ← ВАЖНО
            chat_id=user.telegram_chat_id,
            text="❌ Ваша запись отменена администратором.",
        )


@router.callback_query(F.data.startswith("message_booking:"))
async def message_booking(callback: CallbackQuery) -> None:
    booking_id = int(callback.data.split(":")[1])

    await callback.answer()
    await callback.message.answer(
        f"✉️ Напиши пользователю вручную.\nID записи: {booking_id}"
    )
