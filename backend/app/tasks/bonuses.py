# backend/app/tasks/bonuses.py — celery-задачи бонусов
# Назначение: автоначисление бонусов за завершённые записи

from app.core.celery_app import celery_app
from app.core.database import get_async_session
from app.services.bonuses import apply_bonuses_for_completed_bookings


@celery_app.task
def apply_bonuses_task() -> int:
    """Celery-задача начисления бонусов."""  # (я добавил)

    async def _run() -> int:
        async for db in get_async_session():
            return await apply_bonuses_for_completed_bookings(db)

    import asyncio
    return asyncio.run(_run())
