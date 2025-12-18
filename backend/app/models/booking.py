# backend/app/models/booking.py — модель записи
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Booking(Base):
    """Запись клиента на услугу."""  # (я добавил)

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))

    start_time: Mapped[datetime] = mapped_column(DateTime)  # (я добавил)
