# backend/app/services/salon_settings.py — бизнес-логика настроек салона
# Назначение: получение и обновление глобальных настроек салона

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_settings import SalonSettings


async def get_salon_settings(db: AsyncSession) -> SalonSettings:
    """Получить настройки салона (одна строка)."""  #

    result = await db.execute(select(SalonSettings).where(SalonSettings.id == 1))
    settings = result.scalar_one()

    return settings


async def update_salon_settings(
    db: AsyncSession,
    *,
    work_start_hour: int,
    work_end_hour: int,
    interval_minutes: int,
) -> SalonSettings:
    """Обновить настройки салона."""  #

    result = await db.execute(select(SalonSettings).where(SalonSettings.id == 1))
    settings = result.scalar_one()

    settings.work_start_hour = work_start_hour  #
    settings.work_end_hour = work_end_hour  #
    settings.interval_minutes = interval_minutes  #

    await db.commit()
    await db.refresh(settings)

    return settings
