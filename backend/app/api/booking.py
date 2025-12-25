# backend/app/api/booking.py — эндпоинты онлайн-записи

from datetime import date

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from celery import current_app

from app.core.database import get_db
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate, BookingRead
from app.services.booking import create_booking, get_free_slots


router = APIRouter(
    prefix="/api/booking",
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


@router.post(
    "/{booking_id}/cancel",
    status_code=status.HTTP_200_OK,
)
async def booking_cancel(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Отмена записи."""  # (я добавил)

    result = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking: Booking | None = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    # отменяем запланированные задачи  # (я добавил)
    if booking.reminder_24h_task_id:
        current_app.control.revoke(
            booking.reminder_24h_task_id,
            terminate=False,
        )

    if booking.reminder_2h_task_id:
        current_app.control.revoke(
            booking.reminder_2h_task_id,
            terminate=False,
        )

    booking.status = BookingStatus.CANCELED.value  # (я добавил)
    await db.commit()

    return {"status": "canceled"}
