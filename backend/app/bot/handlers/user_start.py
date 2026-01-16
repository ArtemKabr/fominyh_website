# backend/app/bot/handlers/user_start.py — /start
# Назначение: регистрация пользователя через Telegram

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.user import User
from app.bot.states.user import UserRegister

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext) -> None:
    """Старт и запрос телефона."""  # (я добавил)

    telegram_chat_id = message.from_user.id
    name = message.from_user.first_name or "Пользователь"

    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_chat_id == telegram_chat_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                name=name,
                phone=None,
                email=None,
                telegram_chat_id=telegram_chat_id,
                is_admin=False,
            )
            session.add(user)
            await session.commit()

    await state.set_state(UserRegister.waiting_for_phone)

    await message.answer(
        "👋 Привет!\n\n"
        "Отправь номер телефона, который ты указывал при записи.\n\n"
        "Пример: +79998887766"
    )
