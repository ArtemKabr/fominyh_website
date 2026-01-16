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

router = Router()


@router.message(UserRegister.waiting_for_phone, F.text)
async def phone_handler(message: Message, state: FSMContext) -> None:
    """Сохраняем телефон пользователя с проверкой UNIQUE."""  # (я добавил)

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

        # если номер уже сохранён у этого пользователя
        if user.phone == phone:
            await state.clear()
            await message.answer(
                "✅ Номер уже сохранён.\n\nВыберите действие:",
                reply_markup=user_main_menu_kb(),
            )
            return

        # проверка: номер занят другим пользователем
        exists = await session.scalar(
            select(User).where(User.phone == phone, User.id != user.id)
        )
        if exists:
            await message.answer(
                "❌ Этот номер уже используется другим пользователем.\n"
                "Введите другой номер или обратитесь к администратору."
            )
            return

        user.phone = phone
        await session.commit()

    await state.clear()
    await message.answer(
        "✅ Номер сохранён.\n\nВыберите действие:",
        reply_markup=user_main_menu_kb(),
    )
