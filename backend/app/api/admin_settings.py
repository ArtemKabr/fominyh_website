# backend/app/api/admin_settings.py — настройки салона (админ)
# Назначение: управление рабочим временем и интервалами записи

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import admin_required
from app.models.salon_settings import SalonSettings
from app.models.user import User
from app.schemas.salon_settings import (
    SalonSettingsOut,
    SalonSettingsUpdate,
)

router = APIRouter(
    prefix="/api/admin/settings",
    tags=["admin-settings"],
)


@router.get("/", response_model=SalonSettingsOut)
async def get_salon_settings(
    _: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session),
) -> SalonSettingsOut:
    """Получить настройки салона."""  # (я добавил)

    res = await db.execute(
        select(SalonSettings).where(SalonSettings.id == 1)
    )
    settings = res.scalar_one_or_none()

    if not settings:
        settings = SalonSettings(id=1)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return settings


@router.put("/", response_model=SalonSettingsOut)
async def update_salon_settings(
    payload: SalonSettingsUpdate,
    _: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session),
) -> SalonSettingsOut:
    """Обновить настройки салона."""  # (я добавил)

    res = await db.execute(
        select(SalonSettings).where(SalonSettings.id == 1)
    )
    settings = res.scalar_one_or_none()

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Настройки салона не найдены",
        )

    settings.work_start_hour = payload.work_start_hour
    settings.work_end_hour = payload.work_end_hour
    settings.slot_minutes = payload.slot_minutes

    await db.commit()
    await db.refresh(settings)

    return settings
