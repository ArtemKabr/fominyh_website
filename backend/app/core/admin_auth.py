# backend/app/core/admin_auth.py — защита админ-роутов

from fastapi import Header, HTTPException, status

from app.core.settings import settings  # (я добавил)


def require_admin_token(x_admin_token: str | None = Header(default=None)) -> None:
    """Проверка админского токена из заголовка X-Admin-Token."""  # (я добавил)

    if not x_admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # (я добавил)
            detail="Доступ запрещён: неверный X-Admin-Token",
        )
