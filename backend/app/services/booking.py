# backend/app/services/booking.py — бизнес-логика онлайн-записи
# Назначение: создание, отмена записей и расчёт свободных слотов
from __future__ import annotations

from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.salon_settings import SalonSettings
from app.schemas.booking import AdminSlotBookIn
from app.schemas.booking import BookingCreate
from app.core.redis import redis
from app.core.settings import settings


# -------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -------------------------------------------------


async def _get_service(db: AsyncSession, service_id: int) -> Service:
    """Получить услугу или выбросить 404."""
    res = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    service = res.scalar_one_or_none()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )

    return service


async def _get_salon_settings(db: AsyncSession) -> SalonSettings:
    """Получить настройки салона."""
    res = await db.execute(
        select(SalonSettings).where(SalonSettings.id == 1)
    )
    settings_obj = res.scalar_one_or_none()

    if not settings_obj:
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
    """Получить свободные временные слоты на день."""

    service = await _get_service(db, service_id)
    salon = await _get_salon_settings(db)

    duration = timedelta(minutes=service.duration_minutes)

    day_start = datetime.combine(day, time(hour=salon.work_start_hour))
    day_end = datetime.combine(day, time(hour=salon.work_end_hour))

    res = await db.execute(
        select(Booking).where(
            Booking.service_id == service_id,
            Booking.start_time >= day_start,
            Booking.start_time < day_end,
            Booking.status.in_(
                [
                    BookingStatus.PENDING.value,
                    BookingStatus.ACTIVE.value,
                ]
            ),  # (я добавил)
        )
    )

    busy = {
        b.start_time.replace(second=0, microsecond=0)
        for b in res.scalars().all()
    }

    free: list[datetime] = []
    current = day_start

    while current + duration <= day_end:
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
    """Создать запись (гость или пользователь)."""

    start = booking_in.start_time
    if start is None:
        raise HTTPException(
            status_code=400,
            detail="Start time is required",
        )

    if start < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time is in the past",
        )

    await _get_service(db, booking_in.service_id)

    exists = await db.execute(
        select(Booking).where(
            Booking.service_id == booking_in.service_id,
            Booking.start_time == start,
            Booking.status.in_(
                [BookingStatus.PENDING.value, BookingStatus.ACTIVE.value]
            ),
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot already booked",
        )

    booking = Booking(
        user_id=None,  # гость
        service_id=booking_in.service_id,
        start_time=start,
        status=BookingStatus.PENDING.value,

        guest_name=booking_in.user_name,  # (я добавил)
        guest_phone=booking_in.phone,  # (я добавил)
        guest_email=booking_in.email,  # (я добавил)
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    cache_key = f"free_slots:{start.date()}:{booking.service_id}"
    await redis.delete(cache_key)

    if not settings.testing:
        try:
            from app.tasks.notifications import send_booking_created
            send_booking_created.delay(
                booking.id,
                booking_in.user_name,
                booking_in.phone,
                booking_in.email,
            )
        except Exception:
            pass

    return booking


# -------------------------------------------------
# ОТМЕНА ЗАПИСИ
# -------------------------------------------------


async def cancel_booking(
    db: AsyncSession,
    booking_id: int,
) -> Booking:
    """Отмена записи (soft cancel)."""

    res = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking = res.scalar_one_or_none()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking.status = BookingStatus.CANCELED.value
    await db.commit()
    await db.refresh(booking)

    cache_key = (
        f"free_slots:{booking.start_time.date()}:{booking.service_id}"
    )
    await redis.delete(cache_key)

    return booking


# backend/app/services/booking.py

async def get_day_slots_full(
    db: AsyncSession,
    day: date,
    service_id: int,
):
    """Все временные интервалы дня с состоянием."""
    free = await get_free_slots(db, day, service_id)

    result = await db.execute(
        select(Booking).where(
            Booking.service_id == service_id,  # (я добавил)
            Booking.start_time.between(
                datetime.combine(day, time.min),
                datetime.combine(day, time.max),
            ),
            Booking.status.in_(
                [BookingStatus.PENDING.value, BookingStatus.ACTIVE.value]
            ),  # (я добавил)
        )
    )

    booked = {
        b.start_time: {
            "booking_id": b.id,
            "by_admin": b.created_by_admin,
            "comment": b.admin_comment,
        }
        for b in result.scalars()
    }

    slots = []
    for slot in free:
        slots.append({
            "time": slot.strftime("%H:%M"),
            "status": "free",
        })

    for t, info in booked.items():
        slots.append({
            "time": t.strftime("%H:%M"),
            "status": "booked",
            "booking_id": info["booking_id"],
            "by_admin": info["by_admin"],
            "comment": info["comment"],
        })

    return sorted(slots, key=lambda x: x["time"])


async def create_booking_by_admin(  # (я добавил)
    db: AsyncSession,
    booking_in: "AdminSlotBookIn",
) -> Booking:
    """Создать бронь из админки (admin/client)."""  # (я добавил)

    start = booking_in.start_time
    if start is None:
        raise HTTPException(status_code=400, detail="Start time is required")

    await _get_service(db, booking_in.service_id)

    exists = await db.execute(
        select(Booking).where(
            Booking.service_id == booking_in.service_id,
            Booking.start_time == start,
            Booking.status.in_(
                [BookingStatus.PENDING.value, BookingStatus.ACTIVE.value]
            ),
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot already booked",
        )

    if booking_in.mode == "admin":
        guest_name = "Админ"  # (я добавил)
        guest_phone = "—"  # (я добавил)
        guest_email = None  # (я добавил)
        created_by_admin = True  # (я добавил)
        admin_comment = booking_in.comment  # (я добавил)
    else:
        guest_name = booking_in.guest_name or ""  # (я добавил)
        guest_phone = booking_in.guest_phone or ""  # (я добавил)
        guest_email = booking_in.guest_email  # (я добавил)
        created_by_admin = True  # (я добавил)
        admin_comment = booking_in.comment  # (я добавил)

        if not guest_name.strip() or not guest_phone.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="guest_name и guest_phone обязательны для брони за клиента",
            )

    booking = Booking(
        user_id=None,
        service_id=booking_in.service_id,
        start_time=start,
        status=BookingStatus.ACTIVE.value,  # (я добавил) сразу активная в админке
        guest_name=guest_name,
        guest_phone=guest_phone,
        guest_email=guest_email,
        created_by_admin=created_by_admin,
        admin_comment=admin_comment,
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    cache_key = f"free_slots:{start.date()}:{booking.service_id}"
    await redis.delete(cache_key)

    return booking
