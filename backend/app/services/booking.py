# backend/app/services/booking.py — бизнес-логика онлайн-записи
# Назначение: создание, отмена записей и расчёт свободных слотов

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.tasks.notifications import send_booking_created  # (я добавил)


WORK_START_HOUR = 10
WORK_END_HOUR = 20
SLOT_MINUTES = 30


# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------

async def _get_service(db: AsyncSession, service_id: int) -> Service:
    """Получить услугу или выбросить 404."""  # (я добавил)
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
    """Получить пользователя по телефону или создать нового."""  # (я добавил)
    result = await db.execute(
        select(User).where(User.phone == phone)
    )
    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(
        name=name,
        phone=phone,
        email=email,
    )
    db.add(user)
    await db.flush()  # (я добавил)

    return user


# -------------------------------------------------
# СВОБОДНЫЕ СЛОТЫ
# -------------------------------------------------

async def get_free_slots(
    db: AsyncSession,
    day: date,
    service_id: int,
) -> list[datetime]:
    """Получить свободные временные слоты на день."""  # (я добавил)

    service = await _get_service(db, service_id)
    duration = timedelta(minutes=service.duration_minutes)

    day_start = datetime.combine(day, time.min)
    day_end = datetime.combine(day, time.max)

    result = await db.execute(
        select(Booking).where(
            Booking.service_id == service_id,
            Booking.start_time >= day_start,
            Booking.start_time <= day_end,
        )
    )
    bookings = result.scalars().all()

    busy: set[datetime] = set()
    free: set[datetime] = set()

    for booking in bookings:
        if booking.status == BookingStatus.ACTIVE.value:
            busy.add(booking.start_time)
        else:
            # отменённые записи считаем свободными  # (я добавил)
            free.add(booking.start_time.replace(second=0, microsecond=0))

    # базовая сетка (на будущее)
    current = datetime.combine(day, time(hour=WORK_START_HOUR))
    end = datetime.combine(day, time(hour=WORK_END_HOUR))

    while current + duration <= end:
        if current not in busy:
            free.add(current)
        current += timedelta(minutes=SLOT_MINUTES)

    return sorted(free)


# -------------------------------------------------
# СОЗДАНИЕ ЗАПИСИ
# -------------------------------------------------

async def create_booking(
    db: AsyncSession,
    booking_in: BookingCreate,
) -> Booking:
    """Создать запись с защитой от двойного бронирования."""  # (я добавил)

    if booking_in.start_time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time is in the past",
        )

    service = await _get_service(db, booking_in.service_id)

    start = booking_in.start_time.replace(second=0, microsecond=0)

    # нельзя создать активную запись на занятый слот
    result = await db.execute(
        select(Booking).where(
            Booking.service_id == booking_in.service_id,
            Booking.start_time == start,
            Booking.status == BookingStatus.ACTIVE.value,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot already booked",
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
        start_time=start,
        status=BookingStatus.ACTIVE.value,
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    send_booking_created.delay(booking.id)  # (я добавил)

    return booking


# -------------------------------------------------
# ОТМЕНА ЗАПИСИ
# -------------------------------------------------

async def cancel_booking(
    db: AsyncSession,
    booking_id: int,
) -> Booking:
    """Отмена записи (soft cancel)."""  # (я добавил)

    result = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking.status = BookingStatus.CANCELED.value  # (я добавил)
    await db.commit()
    await db.refresh(booking)

    return booking
