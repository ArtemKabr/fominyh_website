# backend/app/commands/create_admin.py — создание администратора через CLI

import asyncio
import getpass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.core.database import get_engine
from app.core.passwords import hash_password
from app.models.user import User


async def main() -> None:
    engine = get_engine()

    async_session_maker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        # проверяем, есть ли уже администратор
        result = await session.execute(
            select(User).where(User.is_admin.is_(True))
        )
        if result.scalar_one_or_none():
            print("Администратор уже существует")
            return

        password = getpass.getpass("Введите пароль администратора: ")

        admin = User(
            name="Admin",
            phone="+70000000000",
            email="admin@example.com",
            password_hash=hash_password(password),  # я добавил
            is_admin=True,
        )

        session.add(admin)
        await session.commit()

        print("Администратор создан")


if __name__ == "__main__":
    asyncio.run(main())
