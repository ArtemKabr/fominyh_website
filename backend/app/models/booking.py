# backend/app/models/booking.py — модель записи (исправление поля времени)

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user import User  # (я добавил)


class BookingStatus(str, Enum):
    """Статусы записи."""  # (я добавил)

    ACTIVE = "active"
    CANCELED = "canceled"


class Booking(Base):
    """Запись клиента на услугу."""  # (я добавил)

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )  # (я добавил)

    user: Mapped[User | None] = relationship("User")  # (я добавил)

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))

    start_time: Mapped[datetime] = mapped_column(DateTime)  # (я изменил)

    status: Mapped[str] = mapped_column(
        String(20),
        default=BookingStatus.ACTIVE.value,
        nullable=False,
    )

    reminder_24h_task_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    reminder_2h_task_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
