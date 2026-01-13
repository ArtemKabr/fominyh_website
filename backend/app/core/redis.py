# backend/app/core/redis.py — клиент Redis
# Назначение: кэширование (отключается в тестах)

from typing import Any

from redis.asyncio import Redis

from app.core.settings import settings


class DummyRedis:
    """Заглушка Redis для тестов."""

    async def get(self, *args, **kwargs) -> None:
        return None

    async def set(self, *args, **kwargs) -> None:
        return None

    async def delete(self, *args, **kwargs) -> None:
        return None

    async def close(self) -> None:
        return None


if settings.testing:  # 
    redis: Any = DummyRedis()  # 
else:
    redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )
