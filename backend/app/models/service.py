# backend/app/models/service.py — модель услуги
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Service(Base):
    """Услуга салона."""  # (я добавил)

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int] = mapped_column(Integer)
