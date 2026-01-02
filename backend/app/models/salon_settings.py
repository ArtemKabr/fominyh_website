# backend/app/models/salon_settings.py — настройки салона
# Назначение: рабочее время и интервал записи

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SalonSettings(Base):
    """Глобальные настройки салона (1 строка)."""

    __tablename__ = "salon_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    work_start_hour: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
    )

    work_end_hour: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=20,
    )

    slot_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )
