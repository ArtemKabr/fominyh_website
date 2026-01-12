# backend/app/commands/create_admin.py
# Команда создания / повышения администратора

import asyncio
import getpass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import get_engine
from app.core.passwords import hash_password
from app.models.user import User


ADMIN_PHONE = "+70000000000"
ADMIN_EMAIL = "admin@test.ru"


async def main() -> None:
    """Создать или обновить администратора."""  #

    password = getpass.getpass("Введите пароль администратора: ")

    engine = get_engine()
    session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_maker() as session:
        result = await session.execute(select(User).where(User.phone == ADMIN_PHONE))
        user = result.scalar_one_or_none()

        if user:
            user.email = ADMIN_EMAIL
            user.password_hash = hash_password(password)
            user.is_admin = True
            print("Администратор обновлён")  #
        else:
            user = User(
                name="Admin",
                phone=ADMIN_PHONE,
                email=ADMIN_EMAIL,
                password_hash=hash_password(password),
                is_admin=True,
            )
            session.add(user)
            print("Администратор создан")  #

        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
