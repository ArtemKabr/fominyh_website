# backend/app/core/database.py — подключение БД и зависимости
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.settings import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


DATABASE_URL = settings.database_url

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Получить engine (нужно для тестов)."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            DATABASE_URL,
            echo=False,
        )
    return _engine


async_session_maker = sessionmaker(
    bind=get_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД."""
    async with async_session_maker() as session:
        yield session
