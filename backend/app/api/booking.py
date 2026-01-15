# backend/app/api/booking.py — API онлайн-записи
# Назначение: HTTP-эндпоинты для работы с записями

from datetime import date
import json

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.redis import redis
from app.models.reserve import Reserve
from app.schemas.reserve import ReserveCreate
from app.schemas.booking import BookingCreate, BookingRead
from app.services.booking import (
    create_booking,
    cancel_booking,
    get_free_slots,
)

router = APIRouter(
    prefix="/api/booking",
    tags=["Booking"],
)


@router.get("/free")
async def schedule_free(
    day: date = Query(..., description="День в формате YYYY-MM-DD"),
    service_id: int = Query(..., description="ID услуги"),
    db: AsyncSession = Depends(get_async_session),
):
    """Свободные слоты на день."""

    cache_key = f"free_slots:{day}:{service_id}"
    cached = await redis.get(cache_key)

    if cached:
        return json.loads(cached)

    slots = await get_free_slots(
        db=db,
        day=day,
        service_id=service_id,
    )

    data = {
        "day": str(day),
        "service_id": service_id,
        "slots": [s.strftime("%H:%M") for s in slots],
    }

    await redis.set(cache_key, json.dumps(data), ex=60)
    return data


@router.post(
    "",
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED,
)
async def booking_create(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(get_async_session),
):
    """Создание записи."""
    return await create_booking(db, booking_in)


@router.post(
    "/{booking_id}/cancel",
    response_model=BookingRead,
)
async def booking_cancel(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Отмена записи."""
    return await cancel_booking(db, booking_id)


@router.post("/reserve")
async def create_reserve(
    payload: ReserveCreate,
    db: AsyncSession = Depends(get_async_session),
):
    """Создать резерв на день."""  # (я добавил)

    reserve = Reserve(**payload.model_dump())
    db.add(reserve)
    await db.commit()

    return {"ok": True}
