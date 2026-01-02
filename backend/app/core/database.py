# backend/app/core/database.py — подключение БД и Base
# Назначение: единая точка работы с Async SQLAlchemy

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
_sessionmaker: sessionmaker | None = None


def get_engine() -> AsyncEngine:
    """Ленивая инициализация AsyncEngine."""  # (я добавил)
    global _engine, _sessionmaker

    if _engine is None:
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
        )
        _sessionmaker = sessionmaker(
            bind=_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async-сессия БД для FastAPI."""  # (я добавил)
    if _sessionmaker is None:
        get_engine()

    async with _sessionmaker() as session:
        yield session


async def shutdown_engine() -> None:
    """Корректное закрытие engine при shutdown."""  # (я добавил)
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
