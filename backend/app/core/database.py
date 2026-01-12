# backend/app/core/database.py — подключение БД и зависимости
# Назначение: создание AsyncEngine и async-сессий

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
    """Единый AsyncEngine для всего проекта."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            DATABASE_URL,
            echo=False,
        )
    return _engine


# ❗ ВАЖНО: возвращаем async_session_maker
async_session_maker = sessionmaker(  # ← КРИТИЧНО
    bind=get_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """DI для FastAPI."""
    async with async_session_maker() as session:
        yield session


get_async_session = get_db


async def shutdown_engine() -> None:
    """Корректное закрытие engine."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
