# backend/app/api/booking.py — API онлайн-записи
# Назначение: HTTP-эндпоинты для работы с записями

from datetime import date
import json  # 

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.redis import redis  # 
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
    """Свободные слоты на день."""  # 

    cache_key = f"free_slots:{day}:{service_id}"  # 
    cached = await redis.get(cache_key)  # 

    if cached:
        return json.loads(cached)  # 

    slots = await get_free_slots(
        db=db,
        day=day,
        service_id=service_id,
    )

    data = {
        "day": str(day),
        "service_id": service_id,
        "slots": [s.isoformat() for s in slots],
    }  # 

    await redis.set(cache_key, json.dumps(data), ex=60)  # 1 минута 
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
    """Создание записи."""  # 

    booking = await create_booking(
        db=db,
        booking_in=booking_in,
    )

    return booking


@router.post(
    "/{booking_id}/cancel",
    response_model=BookingRead,
    status_code=status.HTTP_200_OK,
)
async def booking_cancel(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Отмена записи."""  # 

    booking = await cancel_booking(
        db=db,
        booking_id=booking_id,
    )

    return booking
