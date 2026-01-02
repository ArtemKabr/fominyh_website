# backend/app/core/admin_auth.py — защита админ-роутов

from fastapi import Header, HTTPException, status
from app.core.config import settings


def require_admin_token(x_admin_token: str | None = Header(default=None)) -> None:
    """Проверка админского токена из заголовка X-Admin-Token."""
    if not x_admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неавторизовано: неверный X-Admin-Token",
        )
