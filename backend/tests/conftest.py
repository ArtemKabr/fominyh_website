# backend/tests/conftest.py — фикстуры pytest для API
# Назначение: настройка тестовой БД и клиента FastAPI

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))  # noqa: E402  # (я добавил)

import asyncio  # noqa: E402
import pytest  # noqa: E402
from httpx import AsyncClient  # noqa: E402
from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.main import app  # noqa: E402
from app.core.database import Base, get_async_session  # noqa: E402
from app.core.settings import settings  # noqa: E402


settings.testing = True  # (я добавил)

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db(engine):
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_async_session] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
async def seed_service(db):
    """Создаёт базовую услугу для тестов."""
    from app.models.service import Service

    result = await db.execute(
        select(Service).where(Service.slug == "test-service")
    )
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
