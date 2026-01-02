# backend/app/services/booking.py — бизнес-логика онлайн-записи

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.service import Service
from app.models.user import User
from app.schemas.booking import BookingCreate


WORK_START_HOUR = 10  # начало рабочего дня (я добавил)
WORK_END_HOUR = 20    # конец рабочего дня (я добавил)
SLOT_MINUTES = 30     # шаг сетки слотов (я добавил)


async def _get_service(db: AsyncSession, service_id: int) -> Service:
    """Получить услугу или выбросить 404."""
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
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
    """Получить пользователя по телефону или создать нового."""
    result = await db.execute(
        select(User).where(User.phone == phone)
    )
    user = result.scalar_one_or_none()

    if user is not None:
        return user

    user = User(
        name=name,
        phone=phone,
        email=email,
    )
    db.add(user)
    await db.flush()  # получаем user.id без commit (я добавил)

    return user


async def get_free_slots(
    db: AsyncSession,
    day: date,
    service_id: int | None = None,
) -> list[datetime]:
    """Получить список свободных временных слотов на день."""

    # определяем длительность услуги
    service_duration = timedelta(minutes=SLOT_MINUTES)
    if service_id is not None:
        service = await _get_service(db, service_id)
        service_duration = timedelta(minutes=service.duration_minutes)

    day_start = datetime.combine(
        day, time(hour=WORK_START_HOUR, minute=0)
    )
    day_end = datetime.combine(
        day, time(hour=WORK_END_HOUR, minute=0)
    )

    # получаем все записи с их услугами на этот день
    result = await db.execute(
        select(Booking, Service)
        .join(Service, Service.id == Booking.service_id)
        .where(
            Booking.start_time >= day_start,
            Booking.start_time < day_end,
        )
    )

    busy_ranges: list[tuple[datetime, datetime]] = []
    for booking, service in result.all():
        start = booking.start_time
        end = start + timedelta(minutes=service.duration_minutes)
        busy_ranges.append((start, end))

    slots: list[datetime] = []
    current = day_start
    now = datetime.now()

    # перебираем сетку слотов
    while current + service_duration <= day_end:
        if current >= now:
            overlap = False
            for busy_start, busy_end in busy_ranges:
                if busy_start < current + service_duration and busy_end > current:
                    overlap = True
                    break

            if not overlap:
                slots.append(current)

        current += timedelta(minutes=SLOT_MINUTES)  # шаг сетки (я добавил)

    return slots


async def create_booking(
    db: AsyncSession,
    booking_in: BookingCreate,
) -> Booking:
    """Создать запись с защитой от пересечений."""

    if booking_in.start_time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time is in the past",
        )

    service = await _get_service(db, booking_in.service_id)
    duration = timedelta(minutes=service.duration_minutes)

    booking_start = booking_in.start_time
    booking_end = booking_start + duration

    # проверка пересечений с существующими записями
    result = await db.execute(
        select(Booking, Service)
        .join(Service, Service.id == Booking.service_id)
        .where(
            Booking.start_time < booking_end,
            (Booking.start_time + timedelta(minutes=Service.duration_minutes))
            > booking_start,
        )
    )

    if result.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot overlaps with existing booking",
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
        start_time=booking_start,
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return booking
