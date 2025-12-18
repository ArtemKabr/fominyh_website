# backend/app/api/booking.py — эндпоинты онлайн-записи

from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.booking import BookingCreate, BookingRead
from app.services.booking import create_booking, get_free_slots

router = APIRouter(
    prefix="/api/booking",   # ВАЖНО
    tags=["Booking"],
)


@router.get("/free")
async def schedule_free(
    day: date = Query(..., description="День в формате YYYY-MM-DD"),
    service_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Свободные слоты на день."""
    slots = await get_free_slots(db=db, day=day, service_id=service_id)
    return {"day": day, "service_id": service_id, "slots": slots}


@router.post(
    "",
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED,
)
async def booking_create(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создание записи."""
    return await create_booking(db=db, booking_in=booking_in)
