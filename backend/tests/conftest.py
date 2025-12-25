# backend/tests/conftest.py — фикстуры pytest для FastAPI
import os
import sys
from pathlib import Path

import pytest_asyncio
from httpx import AsyncClient

# -----------------------------
# TEST ENV (до импорта app)
# -----------------------------
os.environ.setdefault("DEBUG", "True")

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")

os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")

os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/0")
os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# -----------------------------
# PYTHONPATH
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def client():
    """Async HTTP-клиент FastAPI для тестов."""  # (я добавил)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
