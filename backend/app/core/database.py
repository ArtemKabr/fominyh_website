# backend/app/core/database.py — подключение БД и Base
# Назначение: lazy-инициализация engine внутри event loop

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


_engine: AsyncEngine | None = None
_session_maker: sessionmaker | None = None


def get_engine() -> AsyncEngine:
    """Ленивая инициализация engine."""
    global _engine, _session_maker

    if _engine is None:
        _engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
        _session_maker = sessionmaker(
            bind=_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Сессия БД на запрос."""
    if _session_maker is None:
        get_engine()

    async with _session_maker() as session:
        yield session


# alias для FastAPI dependencies
get_async_session = get_db


async def shutdown_engine() -> None:
    """Корректное закрытие engine."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
