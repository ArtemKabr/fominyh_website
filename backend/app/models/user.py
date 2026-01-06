# backend/app/models/user.py — модель пользователя (клиент + auth)

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """Пользователь системы (клиент салона + авторизация)."""  # (я добавил)

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Клиентские данные
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Auth
    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,  # для клиентов без логина
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)  # (я добавил)
