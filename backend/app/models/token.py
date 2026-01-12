# backend/app/models/token.py — модель токенов подтверждения
# Назначение: токены подтверждения email и сброса пароля

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VerificationToken(Base):
    """Токен подтверждения email / сброса пароля."""

    __tablename__ = "verification_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
    )

    def is_expired(self) -> bool:
        """Проверка истечения токена."""
        return datetime.utcnow() > self.expires_at
