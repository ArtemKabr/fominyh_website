# backend/app/models/reserve.py — резерв записей
# Назначение: хранение заявок в резерв при отсутствии слотов

from datetime import date, datetime

from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Reserve(Base):
    """Резервная заявка клиента."""  # (я добавил)

    __tablename__ = "reserves"

    id: Mapped[int] = mapped_column(primary_key=True)

    service_id: Mapped[int] = mapped_column(nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
