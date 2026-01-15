# backend/app/api/user.py — эндпоинты ЛК пользователя
# Назначение: личный кабинет (аватар, профиль, записи) без JWT

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    UploadFile,
    File,
)
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import os
import uuid

from app.core.database import get_async_session
from app.models.user import User
from app.models.booking import Booking, BookingStatus


router = APIRouter(
    prefix="/api/user",
    tags=["user"],
)


async def get_user_by_header(
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    """Получение пользователя по X-User-Id."""

    if not x_user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")

    user = await db.get(User, x_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    return user


@router.get("/dashboard")
async def user_dashboard(
    user: User = Depends(get_user_by_header),
    db: AsyncSession = Depends(get_async_session),
) -> dict:
    """Главная страница ЛК пользователя."""

    total = await db.scalar(
        select(func.count()).where(Booking.user_id == user.id)
    )

    active = await db.scalar(
        select(func.count()).where(
            Booking.user_id == user.id,
            Booking.status == BookingStatus.ACTIVE.value,
        )
    )

    canceled = await db.scalar(
        select(func.count()).where(
            Booking.user_id == user.id,
            Booking.status == BookingStatus.CANCELED.value,
        )
    )

    return {
        "profile": {
            "name": user.name,
            "phone": user.phone,
            "email": user.email,
            "avatar_url": user.avatar_url,
        },
        "stats": {
            "total": total,
            "active": active,
            "canceled": canceled,
        },
        "card": {
            "number": user.card_number,
            "discount_percent": user.discount_percent,
            "bonus_balance": user.bonus_balance,
        },
    }


@router.get("/bookings")
async def user_bookings(
    user: User = Depends(get_user_by_header),
    db: AsyncSession = Depends(get_async_session),
) -> list[dict]:
    """Список записей текущего пользователя."""

    result = await db.execute(
        select(Booking)
        .where(Booking.user_id == user.id)
        .order_by(Booking.start_time.desc())
    )

    bookings = result.scalars().all()

    return [
        {
            "id": b.id,
            "service_name": b.service.name,
            "price": b.service.price,
            "duration_minutes": b.service.duration_minutes,
            "start_at": b.start_time,
            "status": b.status,
        }
        for b in bookings
    ]


@router.post("/bookings/{booking_id}/cancel")
async def cancel_user_booking(
    booking_id: int,
    user: User = Depends(get_user_by_header),
    db: AsyncSession = Depends(get_async_session),
) -> dict:
    """Отмена записи пользователем."""

    booking = await db.get(Booking, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    if booking.status != BookingStatus.ACTIVE.value:
        raise HTTPException(status_code=400, detail="Запись уже отменена")

    booking.status = BookingStatus.CANCELED.value
    await db.commit()

    return {
        "ok": True,
        "booking_id": booking.id,
        "status": booking.status,
    }


@router.put("/profile")
async def update_profile(
    payload: dict,
    user: User = Depends(get_user_by_header),
    db: AsyncSession = Depends(get_async_session),
):
    """Редактирование профиля пользователя."""

    for field in ("name", "phone", "email"):
        if field in payload:
            setattr(user, field, payload[field])

    await db.commit()
    await db.refresh(user)

    return {
        "ok": True,
        "profile": {
            "name": user.name,
            "phone": user.phone,
            "email": user.email,
            "avatar_url": user.avatar_url,
        },
    }


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    user: User = Depends(get_user_by_header),
    db: AsyncSession = Depends(get_async_session),
):
    """Загрузка аватарки пользователя."""  # (я добавил)

    base_dir = "media/avatars"
    os.makedirs(base_dir, exist_ok=True)  # (я добавил)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(base_dir, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    user.avatar_url = f"/media/avatars/{filename}"  # ВАЖНО
    await db.commit()

    return {
        "avatar_url": user.avatar_url,
    }
