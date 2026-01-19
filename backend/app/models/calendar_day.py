# backend/app/models/calendar_day.py — календарные дни
# Назначение: выходные, праздники, кастомное рабочее время

from datetime import date

from sqlalchemy import Date, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CalendarDay(Base):
    __tablename__ = "calendar_days"

    day: Mapped[date] = mapped_column(Date, primary_key=True)

    is_working: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    work_start_hour: Mapped[int | None] = mapped_column(Integer)
    work_end_hour: Mapped[int | None] = mapped_column(Integer)
