# backend/app/core/database.py — подключение к PostgreSQL

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Зависимость FastAPI для получения сессии БД."""
    async with AsyncSessionLocal() as session:
        yield session
