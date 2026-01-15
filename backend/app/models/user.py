# backend/app/models/user.py — модель пользователя
# Назначение: пользователь + данные для ЛК

from sqlalchemy import Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """Пользователь системы (клиент салона + ЛК)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Клиентские данные
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Auth
    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # ЛК / бонусы
    card_number: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )  # (я изменил)

    discount_percent: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )  # (я добавил)

    bonus_balance: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )  # (я добавил)

    avatar_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )  # (я добавил)
