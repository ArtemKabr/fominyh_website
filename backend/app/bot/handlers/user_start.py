# backend/app/bot/handlers/user_start.py — обработчики пользователя
# Назначение: /start и привязка telegram_chat_id

from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select

from app.core.database import get_async_session
from app.models.user import User

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    await message.answer(
        "Привет!\n"
        "Отправь номер телефона, который ты указывал при записи.\n\n"
        "Пример: `+79998887766`"
    )


@router.message()
async def phone_handler(message: types.Message) -> None:
    phone = message.text.strip()
    chat_id = message.chat.id

    async for session in get_async_session():
        result = await session.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()

        if not user:
            await message.answer(
                "Пользователь с таким телефоном не найден.\n"
                "Проверь номер или запишись на сайте."
            )
            return

        user.telegram_chat_id = chat_id
        await session.commit()

    await message.answer(
        "Готово! ✅\n"
        "Telegram успешно привязан.\n\n"
        "Теперь ты будешь получать уведомления."
    )
