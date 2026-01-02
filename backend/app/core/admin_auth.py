# backend/app/core/admin_auth.py — защита админ-роутов

from fastapi import Header, HTTPException, status
from app.core.config import settings


def require_admin_token(x_admin_token: str | None = Header(default=None)) -> None:
    """Проверка админского токена из заголовка X-Admin-Token."""  # (я добавил)
    if not x_admin_token or x_admin_token != settings.admin_token:  # (я добавил)
        raise HTTPException(  # (я добавил)
            status_code=status.HTTP_401_UNAUTHORIZED,  # (я добавил)
            detail="Неавторизовано: неверный X-Admin-Token",  # (я добавил)
        )  # (я добавил)
