# backend/app/commands/create_admin.py — команда создания администратора
# зайти в контенер бекенда
# docker exec -it fominyh_backend bash
# и запустить команду python -m app.commands.create_admin
# Назначение: создать или обновить администратора салона

import asyncio
import getpass
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import get_engine
from app.core.passwords import hash_password
from app.models.user import User


ADMIN_PHONE = "+79811221756"
ADMIN_EMAIL = "admin@mail.ru"
ADMIN_NAME = "Администратор"


async def main() -> None:
    """Создать или обновить администратора."""  # (я добавил)

    password = getpass.getpass("Введите пароль администратора: ")

    engine = get_engine()
    session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_maker() as session:
        result = await session.execute(
            select(User).where(User.phone == ADMIN_PHONE)
        )
        user = result.scalar_one_or_none()

        if user:
            user.email = ADMIN_EMAIL
            user.password_hash = hash_password(password)
            user.is_admin = True
            print("Администратор обновлён")  # (я добавил)
        else:
            user = User(
                name=ADMIN_NAME,
                phone=ADMIN_PHONE,
                email=ADMIN_EMAIL,
                password_hash=hash_password(password),
                is_admin=True,
                card_number=f"ADMIN-{uuid.uuid4().hex[:8]}",  # ← ВАЖНО
                discount_percent=0,
                bonus_balance=0,
            )
            session.add(user)
            print("Администратор создан")  # (я добавил)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
