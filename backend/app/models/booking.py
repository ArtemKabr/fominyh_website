# backend/app/models/booking.py — модель записи
# Назначение: хранение записей клиентов на услуги

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, Boolean  # (я добавил)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user import User
from app.models.service import Service


class BookingStatus(str, Enum):
    """Статусы записи."""

    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"


class Booking(Base):
    """Запись клиента на услугу."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    user: Mapped[User | None] = relationship(
        "User",
        backref="bookings",
    )  # (я добавил)

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False,
    )

    service: Mapped[Service] = relationship(
        "Service",
        backref="bookings",
    )  # (я добавил)

    # В БД колонка start_at, в коде используем start_time
    start_time: Mapped[datetime] = mapped_column(
        "start_at",
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default=BookingStatus.PENDING.value,
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

    guest_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )  # (я добавил)

    guest_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )  # (я добавил)

    guest_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )  # (я добавил)

    created_by_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )  # (я добавил)

    admin_comment: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )  # (я добавил)
