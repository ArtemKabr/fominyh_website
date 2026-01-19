# backend/app/bot/handlers/user_phone.py — приём телефона пользователя
# Назначение: сохранение номера телефона с проверкой уникальности

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.user import User
from app.bot.states.user import UserRegister
from app.bot.keyboards.user import user_main_menu_kb
from app.models.booking import Booking, BookingStatus

router = Router()


@router.message(UserRegister.waiting_for_phone, F.text)
async def phone_handler(message: Message, state: FSMContext) -> None:
    """Сохраняем телефон пользователя с привязкой записей."""  # (я добавил)

    phone = message.text.strip()
    telegram_chat_id = message.from_user.id

    async with async_session_maker() as session:
        user = await session.scalar(
            select(User).where(User.telegram_chat_id == telegram_chat_id)
        )

        if not user:
            await message.answer("Ошибка регистрации. Нажмите /start ещё раз.")
            await state.clear()
            return

        if user.phone == phone:
            await state.clear()
            await message.answer(
                "✅ Номер уже сохранён.\n\nВыберите действие:",
                reply_markup=user_main_menu_kb(),
            )
            return

        exists = await session.scalar(
            select(User).where(User.phone == phone, User.id != user.id)
        )
        if exists:
            await message.answer(
                "❌ Этот номер уже используется другим пользователем.\n"
                "Введите другой номер или обратитесь к администратору."
            )
            return

        # ищем записи, созданные ранее с сайта
        bookings = (
            await session.execute(
                select(Booking)
                .join(User, User.id == Booking.user_id)
                .where(
                    User.phone == phone,
                    User.telegram_chat_id.is_(None),
                    Booking.status == BookingStatus.PENDING.value,
                )
            )
        ).scalars().all()  # (я добавил)

        # сохраняем телефон Telegram-пользователю
        user.phone = phone  # (я добавил)

        # привязываем старые записи
        for booking in bookings:
            booking_user = await session.get(User, booking.user_id)
            booking_user.telegram_chat_id = telegram_chat_id  # (я добавил)

        await session.commit()  # (я добавил)

    await state.clear()
    await message.answer(
        f"✅ Номер сохранён.\n\n"
        f"Найдено записей: {len(bookings)}.\n"
        "⏳ Запись ещё не подтверждена администратором.\n"
        "В ближайшее время администратор проверит её.\n"
        "После подтверждения вам придёт сообщение в Telegram.\n\n"
        "Выберите действие:",
        reply_markup=user_main_menu_kb(),
    )
