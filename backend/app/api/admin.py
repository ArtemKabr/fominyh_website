# backend/app/api/admin.py — админские эндпоинты

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_auth import require_admin_token
from app.core.database import get_async_session
from app.models.service import Service
from app.models.booking import Booking

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin_token)],
)

# ---------- SERVICES ----------

@router.get("/services")
async def admin_list_services(db: AsyncSession = Depends(get_async_session)) -> list[dict]:
    """Список услуг (админ)."""  # (я добавил)
    res = await db.execute(select(Service).order_by(Service.id))
    return [
        {
            "id": s.id,
            "name": s.name,
            "price": s.price,
            "duration_minutes": s.duration_minutes,
            "is_active": getattr(s, "is_active", True),
        }
        for s in res.scalars().all()
    ]


@router.post("/services", status_code=status.HTTP_201_CREATED)
async def admin_create_service(payload: dict, db: AsyncSession = Depends(get_async_session)) -> dict:
    """Создание услуги (админ)."""  # (я добавил)
    service = Service(**payload)
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return {"id": service.id}


@router.put("/services/{service_id}")
async def admin_update_service(
    service_id: int, payload: dict, db: AsyncSession = Depends(get_async_session)
) -> dict:
    """Обновление услуги (админ)."""  # (я добавил)
    res = await db.execute(select(Service).where(Service.id == service_id))
    service = res.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    for k, v in payload.items():
        if hasattr(service, k):
            setattr(service, k, v)
    await db.commit()
    return {"ok": True}


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_service(service_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    """Удаление услуги (админ)."""  # (я добавил)
    await db.execute(delete(Service).where(Service.id == service_id))
    await db.commit()

# ---------- BOOKINGS ----------

@router.get("/bookings")
async def admin_list_bookings(
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    service_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    """Список записей (админ)."""  # (я добавил)
    stmt = select(Booking).order_by(Booking.id)
    if date_from:
        stmt = stmt.where(Booking.start_at >= date_from)
    if date_to:
        stmt = stmt.where(Booking.start_at <= date_to)
    if service_id:
        stmt = stmt.where(Booking.service_id == service_id)
    res = await db.execute(stmt)
    return [
        {
            "id": b.id,
            "service_id": b.service_id,
            "start_at": b.start_at,
            "end_at": b.end_at,
            "status": getattr(b, "status", None),
            "client_name": getattr(b, "client_name", None),
            "client_phone": getattr(b, "client_phone", None),
        }
        for b in res.scalars().all()
    ]


@router.post("/bookings/{booking_id}/cancel")
async def admin_cancel_booking(booking_id: int, db: AsyncSession = Depends(get_async_session)) -> dict:
    """Отмена записи (админ)."""  # (я добавил)
    res = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = res.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if hasattr(booking, "status"):
        booking.status = "cancelled"  # (я добавил)
    await db.commit()
    return {"ok": True}
