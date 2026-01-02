# backend/app/models/booking.py — модель записи

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BookingStatus(str, Enum):
    """Статусы записи."""

    ACTIVE = "active"
    CANCELED = "canceled"


class Booking(Base):
    """Запись клиента на услугу."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))

    start_time: Mapped[datetime] = mapped_column(DateTime)

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
