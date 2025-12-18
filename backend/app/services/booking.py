# backend/app/services/booking.py — бизнес-логика записи # (я добавил)

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.service import Service
from app.models.user import User
from app.schemas.booking import BookingCreate


WORK_START_HOUR = 10  # (я добавил)
WORK_END_HOUR = 20  # (я добавил)
SLOT_MINUTES = 30  # (я добавил)


async def _get_service(db: AsyncSession, service_id: int) -> Service:
    """Получить услугу или поднять 404."""  # (я добавил)
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    return service


async def _get_or_create_user(
    db: AsyncSession,
    name: str,
    phone: str,
    email: str | None,
) -> User:
    """Получить пользователя по телефону или создать нового."""  # (я добавил)
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if user is not None:
        return user

    user = User(name=name, phone=phone, email=email)
    db.add(user)
    await db.flush()  # (я добавил) получаем user.id без отдельного commit
    return user


async def get_free_slots(
    db: AsyncSession,
    day: date,
    service_id: int | None = None,
) -> list[datetime]:
    """Получить свободные слоты на день."""  # (я добавил)
    step_minutes = SLOT_MINUTES  # (я добавил)
    if service_id is not None:
        service = await _get_service(db, service_id)
        step_minutes = max(int(service.duration_minutes), SLOT_MINUTES)  # (я добавил)

    day_start = datetime.combine(day, time(hour=WORK_START_HOUR, minute=0))
    day_end = datetime.combine(day, time(hour=WORK_END_HOUR, minute=0))

    # Забираем занятые слоты на этот день
    result = await db.execute(
        select(Booking.start_time).where(
            Booking.start_time >= day_start,
            Booking.start_time < day_end,
        )
    )
    busy = {row[0] for row in result.all()}  # (я добавил)

    slots: list[datetime] = []  # (я добавил)
    current = day_start
    step = timedelta(minutes=step_minutes)
    now = datetime.now()

    while current + step <= day_end:
        if current not in busy and current >= now:
            slots.append(current)
        current += timedelta(minutes=SLOT_MINUTES)  # (я добавил) шаг сетки фиксированный

    return slots


async def create_booking(db: AsyncSession, booking_in: BookingCreate) -> Booking:
    """Создать запись с защитой от двойной записи."""  # (я добавил)
    if booking_in.start_time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time is in the past",
        )

    await _get_service(db, booking_in.service_id)

    # Защита от двойной записи (по точному времени старта)
    result = await db.execute(
        select(Booking).where(Booking.start_time == booking_in.start_time)
    )
    exists = result.scalar_one_or_none()
    if exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot is already booked",
        )

    user = await _get_or_create_user(
        db=db,
        name=booking_in.user_name,
        phone=booking_in.phone,
        email=booking_in.email,
    )

    booking = Booking(
        user_id=user.id,
        service_id=booking_in.service_id,
        start_time=booking_in.start_time,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking
