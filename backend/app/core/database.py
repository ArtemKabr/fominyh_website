# backend/app/core/database.py — подключение БД и Base
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.settings import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""  # (я добавил)


DATABASE_URL = settings.database_url  # (я добавил)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД."""  # (я добавил)
    async with async_session_maker() as session:
        yield session
