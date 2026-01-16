# backend/app/models/user.py — модель пользователя

from sqlalchemy import Boolean, String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """Пользователь системы (клиент салона + ЛК)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    phone: Mapped[str | None] = mapped_column(  # ← ИЗМЕНЕНО
        String(20),
        unique=True,
        nullable=True,  # (я добавил)
    )

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    telegram_chat_id: Mapped[int | None] = mapped_column(
        BigInteger,
        unique=True,
        nullable=True,
    )

    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    card_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    discount_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bonus_balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
