# backend/tests/conftest.py — фикстуры pytest
# Назначение: тестовая БД (NullPool) + очистка БД + HTTP-клиент + JWT + отключение Celery

import os
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import delete


# ---------------------------------------------------------------------
# ENV для тестов
# ---------------------------------------------------------------------

os.environ.setdefault("DB_HOST", "db")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "fominyh_db")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")


# ---------------------------------------------------------------------
# TEST ENGINE
# ---------------------------------------------------------------------

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Единый async engine для всех тестов (NullPool)."""
    from app.core.settings import settings
    from app.core.database import Base

    engine = create_async_engine(
        settings.database_url,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


# ---------------------------------------------------------------------
# OVERRIDE DATABASE
# ---------------------------------------------------------------------

@pytest_asyncio.fixture(autouse=True)
async def override_database(test_engine, monkeypatch):
    """Подмена get_engine / get_db."""
    from app.core import database

    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    monkeypatch.setattr(database, "get_engine", lambda: test_engine)

    async def _get_db():
        async with async_session() as session:
            yield session

    monkeypatch.setattr(database, "get_db", _get_db)


# ---------------------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def app():
    from app.main import app as fastapi_app
    return fastapi_app


# ---------------------------------------------------------------------
# HTTP CLIENTS
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def client(app):
    """Основной клиент (нужен booking/services тестам)."""  # (я добавил)
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as c:
        yield c


@pytest_asyncio.fixture
async def async_client(client):
    """Алиас async_client."""  # (я добавил)
    yield client


# ---------------------------------------------------------------------
# DISABLE CELERY
# ---------------------------------------------------------------------

@pytest.fixture(autouse=True)
def disable_celery(monkeypatch):
    monkeypatch.setattr(
        "app.tasks.notifications.send_booking_created.delay",
        lambda *args, **kwargs: None,
    )


# ---------------------------------------------------------------------
# CLEAN DATABASE
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def clean_db(test_engine):
    """Очистка БД с учётом FK."""  # (я добавил)
    from app.models.booking import Booking
    from app.models.user import User

    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        await session.execute(delete(Booking))
        await session.execute(delete(User))
        await session.commit()


# ---------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def admin_user(clean_db, test_engine):
    """Администратор."""  # (я добавил)
    from app.models.user import User
    from app.core.passwords import hash_password

    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        user = User(
            name="Admin",
            phone="+79990000001",
            email="admin@test.ru",
            password_hash=hash_password("admin_password"),
            is_admin=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def regular_user(clean_db, test_engine):
    """Обычный пользователь."""  # (я добавил)
    from app.models.user import User
    from app.core.passwords import hash_password

    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        user = User(
            name="User",
            phone="+79990000002",
            email="user@test.ru",
            password_hash=hash_password("user_password"),
            is_admin=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


# ---------------------------------------------------------------------
# TOKENS
# ---------------------------------------------------------------------

@pytest_asyncio.fixture
async def admin_token(async_client, admin_user):
    resp = await async_client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "admin_password"},
    )
    return resp.json()["access_token"]


@pytest_asyncio.fixture
async def user_token(async_client, regular_user):
    resp = await async_client.post(
        "/api/auth/login",
        json={"email": regular_user.email, "password": "user_password"},
    )
    return resp.json()["access_token"]
