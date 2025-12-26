# backend/tests/conftest.py — фикстуры pytest
# Назначение: тестовая БД (NullPool) + override get_engine/get_db + HTTP-клиент + отключение Celery

import os
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


# ---------------------------------------------------------------------
# ENV для тестов
# ---------------------------------------------------------------------

os.environ.setdefault("DB_HOST", "db")            # (я добавил)
os.environ.setdefault("DB_PORT", "5432")          # (я добавил)
os.environ.setdefault("DB_NAME", "fominyh_db")    # (я добавил)
os.environ.setdefault("DB_USER", "postgres")      # (я добавил)
os.environ.setdefault("DB_PASSWORD", "postgres")  # (я добавил)


# ---------------------------------------------------------------------
# TEST ENGINE — ЕДИНСТВЕННЫЙ, БЕЗ POOL
# ---------------------------------------------------------------------

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Единый async engine для всех тестов (NullPool)."""  # (я добавил)
    from app.core.settings import settings
    from app.core.database import Base

    engine = create_async_engine(
        settings.database_url,
        echo=False,
        poolclass=NullPool,  # (я добавил)
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # (я добавил)

    yield engine

    await engine.dispose()  # (я добавил)


# ---------------------------------------------------------------------
# OVERRIDE DATABASE (FUNCTION + AUTO)
# ---------------------------------------------------------------------

@pytest_asyncio.fixture(autouse=True)
async def override_database(test_engine, monkeypatch):
    """Полная подмена engine и get_db на тестовые."""  # (я добавил)
    from app.core import database

    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # get_engine -> test_engine
    monkeypatch.setattr(database, "get_engine", lambda: test_engine)  # (я добавил)

    # get_db -> session from test_engine
    async def _get_db():
        async with async_session() as session:
            yield session

    monkeypatch.setattr(database, "get_db", _get_db)  # (я добавил)


# ---------------------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def app():
    """FastAPI приложение."""  # (я добавил)
    from app.main import app as fastapi_app
    return fastapi_app


# ---------------------------------------------------------------------
# HTTP CLIENT
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def client(app):
    """HTTP-клиент FastAPI."""  # (я добавил)
    transport = ASGITransport(app=app)  # (я добавил)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


# ---------------------------------------------------------------------
# DISABLE CELERY
# ---------------------------------------------------------------------

@pytest.fixture(autouse=True)
def disable_celery(monkeypatch):
    """Отключаем Celery-задачи в тестах."""  # (я добавил)
    monkeypatch.setattr(
        "app.tasks.notifications.send_booking_created.delay",
        lambda *args, **kwargs: None,
    )
