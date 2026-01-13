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
from app.models.salon_settings import SalonSettings
from app.schemas.booking import BookingCreate
from app.core.settings import settings
from app.core.redis import redis  # 


# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------


async def _get_service(db: AsyncSession, service_id: int) -> Service:
    """Получить услугу или выбросить 404."""

    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()

    if not service:
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
    """Получить пользователя по телефону или создать нового."""  # 

    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(
        name=name,
        phone=phone,
        email=email,
        password_hash="",  # 
        is_admin=False,  # 
    )

    db.add(user)
    await db.flush()

    return user


async def _get_salon_settings(db: AsyncSession) -> SalonSettings:
    """Получить настройки салона."""  # 

    result = await db.execute(select(SalonSettings).where(SalonSettings.id == 1))
    settings_obj = result.scalar_one_or_none()

    if settings_obj is None:
        settings_obj = SalonSettings(id=1)
        db.add(settings_obj)
        await db.commit()
        await db.refresh(settings_obj)

    return settings_obj


# -------------------------------------------------
# СВОБОДНЫЕ СЛОТЫ
# -------------------------------------------------


async def get_free_slots(
    db: AsyncSession,
    day: date,
    service_id: int,
) -> list[datetime]:
    """Получить свободные временные слоты на день."""  # 

    service = await _get_service(db, service_id)
    salon = await _get_salon_settings(db)

    duration = timedelta(minutes=service.duration_minutes)

    day_start = datetime.combine(day, time.min)
    day_end = datetime.combine(day, time.max)

    result = await db.execute(
        select(Booking).where(
            Booking.service_id == service_id,
            Booking.start_time >= day_start,
            Booking.start_time <= day_end,
            Booking.status == BookingStatus.ACTIVE.value,
        )
    )
    bookings = result.scalars().all()

    busy: set[datetime] = {
        b.start_time.replace(second=0, microsecond=0) for b in bookings
    }  # 

    free: list[datetime] = []

    current = datetime.combine(day, time(hour=salon.work_start_hour))
    end = datetime.combine(day, time(hour=salon.work_end_hour))

    while current + duration <= end:
        if current not in busy:
            free.append(current)
        current += timedelta(minutes=salon.interval_minutes)

    return free


# -------------------------------------------------
# СОЗДАНИЕ ЗАПИСИ
# -------------------------------------------------


async def create_booking(
    db: AsyncSession,
    booking_in: BookingCreate,
) -> Booking:
    """Создать запись с защитой от двойного бронирования."""  # 

    start = booking_in.start_time.replace(
        tzinfo=None,
        second=0,
        microsecond=0,
    )

    if start < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time is in the past",
        )

    await _get_service(db, booking_in.service_id)

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

    # инвалидация кеша слотов
    cache_key = f"free_slots:{start.date()}:{booking.service_id}"  # 
    await redis.delete(cache_key)  # 

    if not settings.testing:  # 
        from app.tasks.notifications import send_booking_created
        send_booking_created.delay(booking.id)

    return booking


# -------------------------------------------------
# ОТМЕНА ЗАПИСИ
# -------------------------------------------------


async def cancel_booking(
    db: AsyncSession,
    booking_id: int,
) -> Booking:
    """Отмена записи (soft cancel)."""  # 

    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking.status = BookingStatus.CANCELED.value
    await db.commit()
    await db.refresh(booking)

    cache_key = f"free_slots:{booking.start_time.date()}:{booking.service_id}"  # 
    await redis.delete(cache_key)  # 

    return booking
