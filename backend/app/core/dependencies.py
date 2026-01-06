# backend/app/core/dependencies.py — зависимости авторизации
# Назначение: проверка JWT и прав администратора

from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user import User


async def admin_required(
    user: User = Depends(get_current_user),
) -> User:
    """Доступ только для администратора."""  # (я добавил)

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    return user
