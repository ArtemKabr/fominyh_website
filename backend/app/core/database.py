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
    """Получить AsyncEngine (единый для приложения и тестов)."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            DATABASE_URL,
            echo=False,
        )
    return _engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение async-сессии БД."""
    async_session_maker = sessionmaker(
        bind=get_engine(),  # я добавил
        class_=AsyncSession,  # я добавил
        expire_on_commit=False,  # я добавил
    )
    async with async_session_maker() as session:
        yield session


# алиас для совместимости с зависимостями и тестами
get_async_session = get_db  # я добавил


async def shutdown_engine() -> None:
    """Корректное закрытие AsyncEngine при shutdown приложения."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None  # я добавил
