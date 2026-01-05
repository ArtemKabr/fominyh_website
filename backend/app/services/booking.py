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
from app.models.salon_settings import SalonSettings  # (я добавил)
from app.schemas.booking import BookingCreate
from app.tasks.notifications import send_booking_created


# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------


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

    if user:
        return user

    user = User(
        name=name,
        phone=phone,
        email=email,
    )
    db.add(user)
    await db.flush()

    return user


async def _get_salon_settings(db: AsyncSession) -> SalonSettings:
    """Получить настройки салона (всегда одна строка)."""  # (я добавил)
    result = await db.execute(
        select(SalonSettings).where(SalonSettings.id == 1)
    )
    settings = result.scalar_one_or_none()

    if settings is None:
        settings = SalonSettings(id=1)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return settings


# -------------------------------------------------
# СВОБОДНЫЕ СЛОТЫ
# -------------------------------------------------


# backend/app/services/booking.py — бизнес-логика онлайн-записи
# Назначение: создание, отмена записей и расчёт свободных слотов

async def get_free_slots(
    db: AsyncSession,
    day: date,
    service_id: int,
) -> list[datetime]:
    """Получить свободные временные слоты на день."""  # (я исправил)

    service = await _get_service(db, service_id)
    salon = await _get_salon_settings(db)

    duration = timedelta(minutes=service.duration_minutes)

    day_start = datetime.combine(day, time.min)
    day_end = datetime.combine(day, time.max)

    result = await db.execute(
        select(Booking).where(
            Booking.service_id == service_id,
            Booking.start_at >= day_start,
            Booking.start_at <= day_end,
        )
    )
    bookings = result.scalars().all()

    busy: set[datetime] = set()
    released: set[datetime] = set()

    for booking in bookings:
        slot = booking.start_at.replace(second=0, microsecond=0)

        if booking.status == BookingStatus.ACTIVE.value:
            busy.add(slot)
        else:
            released.add(slot)  # (я добавил)

    free: list[datetime] = []

    # стандартная генерация по рабочим часам
    current = datetime.combine(day, time(hour=salon.work_start_hour))
    end = datetime.combine(day, time(hour=salon.work_end_hour))

    while current + duration <= end:
        if current not in busy:
            free.append(current)
        current += timedelta(minutes=salon.interval_minutes)

    # обязательно возвращаем освобождённые слоты
    for slot in released:
        if slot not in busy and slot not in free:
            free.append(slot)  # (я добавил)

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

    await _get_service(db, booking_in.service_id)

    start = booking_in.start_time.replace(second=0, microsecond=0)

    result = await db.execute(
        select(Booking).where(
            Booking.service_id == booking_in.service_id,
            Booking.start_at == start,
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
        start_at=start,  # (я добавил)
        status=BookingStatus.ACTIVE.value,
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    send_booking_created.delay(booking.id)

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

    booking.status = BookingStatus.CANCELED.value
    await db.commit()
    await db.refresh(booking)

    return booking
