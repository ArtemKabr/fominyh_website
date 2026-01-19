# backend/app/api/admin_calendar.py — календарь работы салона (админ)
# Назначение: выходные, праздники, кастомное рабочее время по дням

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import admin_required
from app.models.calendar_day import CalendarDay
from app.models.user import User

router = APIRouter(
    prefix="/api/admin/calendar",
    tags=["admin-calendar"],
)


@router.get("/{day}")
async def get_calendar_day(
    day: date,
    _: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session),
):
    """Получить настройки конкретного дня."""  # (я добавил)

    obj = await db.get(CalendarDay, day)
    if not obj:
        return {
            "day": day,
            "is_working": True,
            "work_start_hour": None,
            "work_end_hour": None,
        }

    return {
        "day": obj.day,
        "is_working": obj.is_working,
        "work_start_hour": obj.work_start_hour,
        "work_end_hour": obj.work_end_hour,
    }


@router.post("")
async def upsert_calendar_day(
    payload: dict,
    _: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Создать или обновить день.

    payload:
    {
        day: YYYY-MM-DD,
        is_working: bool,
        work_start_hour?: int,
        work_end_hour?: int
    }
    """  # (я добавил)

    day = payload.get("day")
    if not day:
        raise HTTPException(
            status_code=400,
            detail="day is required",
        )

    is_working = payload.get("is_working", True)
    work_start = payload.get("work_start_hour")
    work_end = payload.get("work_end_hour")

    # валидация времени
    if is_working:
        if work_start is not None and not (0 <= work_start <= 23):
            raise HTTPException(
                status_code=400,
                detail="work_start_hour must be between 0 and 23",
            )
        if work_end is not None and not (1 <= work_end <= 24):
            raise HTTPException(
                status_code=400,
                detail="work_end_hour must be between 1 and 24",
            )
        if (
            work_start is not None
            and work_end is not None
            and work_start >= work_end
        ):
            raise HTTPException(
                status_code=400,
                detail="work_start_hour must be < work_end_hour",
            )

    obj = await db.get(CalendarDay, day)
    if not obj:
        obj = CalendarDay(day=day)
        db.add(obj)  # (я добавил)

    obj.is_working = is_working
    obj.work_start_hour = work_start
    obj.work_end_hour = work_end

    await db.commit()

    return {"ok": True}


@router.delete("/{day}")
async def delete_calendar_day(
    day: date,
    _: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session),
):
    """Удалить кастомный день (вернуть дефолт)."""  # (я добавил)

    obj = await db.get(CalendarDay, day)
    if obj:
        await db.delete(obj)
        await db.commit()

    return {"ok": True}
