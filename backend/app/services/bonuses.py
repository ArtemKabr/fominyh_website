# backend/app/services/bonuses.py — начисление бонусов
# Назначение: бонусная логика ЛК

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.models.service import Service


async def apply_bonuses_for_completed_bookings(
    db: AsyncSession,
) -> int:
    """
    Начислить бонусы за завершённые записи.
    Возвращает количество обработанных записей.
    """

    result = await db.execute(
        select(Booking, Service, User)
        .join(Service, Service.id == Booking.service_id)
        .join(User, User.id == Booking.user_id)
        .where(
            Booking.status == BookingStatus.ACTIVE.value,
            Booking.start_at < datetime.utcnow(),
        )
    )

    processed = 0

    for booking, service, user in result.all():
        bonus = service.price // 10  # 10% (я добавил)

        user.bonus_balance += bonus
        booking.status = BookingStatus.COMPLETED.value

        processed += 1

    if processed:
        await db.commit()

    return processed
