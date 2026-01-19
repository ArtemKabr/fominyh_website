# backend/app/api/admin.py — админка без JWT
# Назначение: управление записями, пользователями и настройками салона

from typing import Optional
from datetime import date, datetime

from fastapi import APIRouter, HTTPException, Depends, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from app.core.database import get_async_session
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.reserve import Reserve

from app.services.booking import get_day_slots_full, create_booking_by_admin  # (я добавил)
from app.schemas.booking import AdminSlotBookIn  # (я добавил)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# -------------------------------------------------
# DEPENDENCY
# -------------------------------------------------


async def get_admin(
        x_user_id: int = Header(..., alias="X-User-Id"),
        db: AsyncSession = Depends(get_async_session),
) -> User:
    """Проверка прав администратора."""
    res = await db.execute(select(User).where(User.id == x_user_id))
    user = res.scalar_one_or_none()

    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    return user


# -------------------------------------------------
# ЗАПИСИ (НОВЫЕ + ИСТОРИЯ)
# -------------------------------------------------


@router.get("/bookings")
async def admin_get_bookings(
        status: Optional[str] = None,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Все записи клиентов (включая гостей)."""

    query = (
        select(Booking, User, Service)
        .outerjoin(User, Booking.user_id == User.id)
        .join(Service, Booking.service_id == Service.id)
    )

    if status:
        query = query.where(Booking.status == status)

    query = query.order_by(Booking.start_time.desc())

    result = await db.execute(query)

    return [
        {
            "id": b.id,
            "start_time": b.start_time,
            "status": b.status,
            "service": {
                "id": s.id,
                "name": s.name,
                "price": s.price,
            },
            "user": (
                {
                    "id": u.id,
                    "name": u.name,
                    "phone": u.phone,
                    "email": u.email,
                }
                if u else {
                    "id": None,
                    "name": b.guest_name,
                    "phone": b.guest_phone,
                    "email": b.guest_email,
                }
            ),
            "comment": b.guest_comment,  # (я добавил)
        }
        for b, u, s in result.all()
    ]


@router.post("/bookings/{booking_id}/confirm")
async def admin_confirm_booking(
        booking_id: int,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Подтвердить запись."""
    booking = await db.get(Booking, booking_id)

    if not booking:
        raise HTTPException(404, "Запись не найдена")

    if booking.status != BookingStatus.PENDING.value:
        raise HTTPException(400, "Запись уже обработана")

    booking.status = BookingStatus.ACTIVE.value
    await db.commit()

    return {"status": booking.status}


@router.post("/bookings/{booking_id}/cancel")
async def admin_cancel_booking(
        booking_id: int,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Отменить запись."""
    booking = await db.get(Booking, booking_id)

    if not booking:
        raise HTTPException(404, "Запись не найдена")

    if booking.status == BookingStatus.COMPLETED.value:
        raise HTTPException(400, "Завершённую запись нельзя отменить")

    booking.status = BookingStatus.CANCELED.value
    await db.commit()

    return {"status": booking.status}


@router.post("/bookings/history/clear")
async def admin_clear_booking_history(
        admin: User = Depends(get_admin),  # (я исправил)
        db: AsyncSession = Depends(get_async_session),
) -> dict:
    """Очистить историю записей (админ)."""

    await db.execute(
        delete(Booking).where(
            Booking.status.in_(
                [
                    BookingStatus.CANCELED.value,
                    BookingStatus.COMPLETED.value,
                ]
            )
        )
    )

    await db.commit()

    return {"ok": True}


@router.post("/bookings/{booking_id}/reschedule")
async def admin_reschedule_booking(
        booking_id: int,
        new_day: date = Query(...),  # (я добавил)
        new_time: str = Query(...),  # (я добавил)
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Перенести запись на другое время."""  # (я добавил)

    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Запись не найдена")

    if booking.status != BookingStatus.ACTIVE.value:
        raise HTTPException(400, "Перенос возможен только для активных записей")

    try:
        new_start = datetime.fromisoformat(f"{new_day} {new_time}")
    except Exception:
        raise HTTPException(400, "Неверная дата или время")

    # проверка конфликта
    exists = await db.execute(
        select(Booking).where(
            Booking.service_id == booking.service_id,
            Booking.start_time == new_start,
            Booking.status.in_(
                [BookingStatus.PENDING.value, BookingStatus.ACTIVE.value]
            ),
            Booking.id != booking.id,
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(409, "Слот уже занят")

    booking.start_time = new_start
    await db.commit()

    return {"status": "ok"}


# -------------------------------------------------
# КАЛЕНДАРЬ / СЛОТЫ
# -------------------------------------------------


@router.get("/bookings/calendar")
async def admin_bookings_calendar(
        date_from: date,
        date_to: date,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Даты с занятыми слотами (ТОЛЬКО активные записи)."""

    result = await db.execute(
        select(
            func.date(Booking.start_time),
            func.count(Booking.id),
        )
        .where(
            Booking.start_time.between(date_from, date_to),
            Booking.status.in_([
                BookingStatus.PENDING.value,
                BookingStatus.ACTIVE.value,
            ]),  # ← КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ
        )
        .group_by(func.date(Booking.start_time))
    )

    return [
        {"date": str(day), "count": count}
        for day, count in result.all()
    ]


@router.get("/bookings/by-day")
async def admin_bookings_by_day(
        day: date,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Записи на конкретный день."""  # (я добавил)

    result = await db.execute(
        select(Booking, User, Service)
        .outerjoin(User, Booking.user_id == User.id)
        .join(Service, Booking.service_id == Service.id)
        .where(
            func.date(Booking.start_time) == day,
            Booking.status != BookingStatus.CANCELED.value,
        )
        .order_by(Booking.start_time)
    )

    return [
        {
            "id": b.id,
            "start_time": b.start_time,
            "status": b.status,
            "service": {
                "id": s.id,
                "name": s.name,
                "price": s.price,
            },  # (я добавил)
            "user": (
                {
                    "name": u.name,
                    "phone": u.phone,
                    "email": u.email,
                }
                if u else {
                    "name": b.guest_name,
                    "phone": b.guest_phone,
                    "email": b.guest_email,
                }
            ),
            "comment": b.admin_comment,  # (я добавил)
        }
        for b, u, s in result.all()
    ]


# -------------------------------------------------
# СЛОТЫ (АДМИН)
# -------------------------------------------------


@router.get("/slots")
async def admin_day_slots(
        day: date,
        service_id: int,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Все интервалы дня со статусом free/booked."""
    return await get_day_slots_full(db, day, service_id)


@router.post("/slots/book")
async def admin_slot_book(
        payload: AdminSlotBookIn,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Бронь слота из админки (admin/client)."""
    booking = await create_booking_by_admin(db, payload)
    return {"id": booking.id, "status": booking.status}


# -------------------------------------------------
# УСЛУГИ
# -------------------------------------------------


@router.get("/services")
async def admin_services(
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Список услуг."""  # (я добавил)
    res = await db.execute(select(Service).order_by(Service.id))
    return [
        {
            "id": s.id,
            "name": s.name,
            "price": s.price,
            "duration_minutes": s.duration_minutes,
        }
        for s in res.scalars().all()
    ]


@router.post("/services")
async def admin_create_service(
        payload: dict,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Создать услугу."""  # (я добавил)
    service = Service(
        name=payload["name"],
        price=payload["price"],
        duration_minutes=payload.get("duration_minutes"),
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return {"id": service.id}


@router.put("/services/{service_id}")
async def admin_update_service(
        service_id: int,
        payload: dict,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Редактировать услугу."""  # (я добавил)
    service = await db.get(Service, service_id)
    if not service:
        raise HTTPException(404, "Услуга не найдена")

    for field in ("name", "price", "duration_minutes"):
        if field in payload:
            setattr(service, field, payload[field])

    await db.commit()
    return {"ok": True}


@router.delete("/services/{service_id}")
async def admin_delete_service(
        service_id: int,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Удалить услугу."""  # (я добавил)
    await db.execute(delete(Service).where(Service.id == service_id))
    await db.commit()
    return {"ok": True}


# -------------------------------------------------
# КЛИЕНТЫ
# -------------------------------------------------


@router.get("/users")
async def admin_users(
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Список пользователей."""  # (я добавил)
    res = await db.execute(select(User).order_by(User.id))
    return [
        {
            "id": u.id,
            "name": u.name,
            "phone": u.phone,
            "email": u.email,
            "is_admin": u.is_admin,  # (я добавил)
        }
        for u in res.scalars().all()
    ]


# -------------------------------------------------
# СТАТИСТИКА
# -------------------------------------------------


@router.get("/stats")
async def admin_stats(
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Статистика записей."""  # (я добавил)

    total = await db.scalar(
        select(func.count()).select_from(Booking)
    )
    active = await db.scalar(
        select(func.count()).where(
            Booking.status == BookingStatus.ACTIVE.value
        )
    )
    canceled = await db.scalar(
        select(func.count()).where(
            Booking.status == BookingStatus.CANCELED.value
        )
    )

    return {
        "total": total,
        "active": active,
        "canceled": canceled,
    }


# -------------------------------------------------
# РЕЗЕРВ
# -------------------------------------------------


@router.get("/reserve")
async def admin_reserve_list(
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Список резерва."""  # (я добавил)

    res = await db.execute(
        select(Reserve).order_by(Reserve.created_at.desc())
    )

    return [
        {
            "id": r.id,
            "service_id": r.service_id,
            "day": r.day,
            "name": r.name,
            "phone": r.phone,
            "email": r.email,
            "comment": r.comment,
            "created_at": r.created_at,
        }
        for r in res.scalars().all()
    ]


@router.delete("/reserve/{reserve_id}")
async def admin_reserve_delete(
        reserve_id: int,
        admin: User = Depends(get_admin),
        db: AsyncSession = Depends(get_async_session),
):
    """Удалить резерв."""  # (я добавил)

    reserve = await db.get(Reserve, reserve_id)
    if not reserve:
        raise HTTPException(404, "Резерв не найден")

    await db.delete(reserve)
    await db.commit()

    return {"ok": True}
