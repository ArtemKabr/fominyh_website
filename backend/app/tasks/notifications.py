# backend/tests/conftest.py — фикстуры pytest для API

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.main import app
from app.core.database import Base, get_async_session
from app.core.settings import settings

settings.testing = True  # (я добавил)

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # (я добавил)


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

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
async def seed_service(db):
    """Создаёт базовую услугу, если её ещё нет."""  # (я добавил)
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
