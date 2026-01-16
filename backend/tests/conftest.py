# backend/tests/conftest.py — фикстуры pytest
# Назначение: изоляция тестов от Redis и PostgreSQL, корректная работа async
# flake8: noqa  # (я добавил)

import sys  # (я добавил)
from pathlib import Path  # (я добавил)

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))  # (я добавил)

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.core.settings import settings

# -------------------------------------------------
# ВАЖНО: включаем режим тестов ДО импорта app
# -------------------------------------------------
settings.testing = True  # (я добавил)

from app.main import app  # noqa: E402
from app.core.database import Base, get_async_session  # noqa: E402


# -------------------------------------------------
# Заглушка Redis
# -------------------------------------------------
class DummyRedis:
    """Заглушка Redis для тестов."""  # (я добавил)

    async def get(self, *args, **kwargs):
        return None

    async def set(self, *args, **kwargs):
        return None

    async def delete(self, *args, **kwargs):
        return None

    async def close(self):
        return None


@pytest.fixture(autouse=True)
def disable_redis(monkeypatch):
    """Отключает Redis во всех тестах."""  # (я добавил)
    monkeypatch.setattr(
        "app.core.redis.redis",
        DummyRedis(),
    )


# -------------------------------------------------
# Тестовая БД (SQLite in-memory)
# -------------------------------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # (я добавил)


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db(engine):
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_async_session] = override_get_db

    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client


# -------------------------------------------------
# Начальные данные
# -------------------------------------------------
@pytest_asyncio.fixture(autouse=True)
async def seed_service(db):
    """Создаёт базовую услугу для тестов."""  # (я добавил)
    from app.models.service import Service

    result = await db.execute(select(Service).where(Service.slug == "test-service"))
    service = result.scalar_one_or_none()

    if service:
        return service

    service = Service(
        name="Тестовая услуга",
        slug="test-service",
        category="face",
        price=1000,
        duration_minutes=60,
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service
