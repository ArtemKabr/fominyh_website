# backend/app/api/deps.py — зависимости авторизации

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.settings import settings
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_async_session),
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    """Получить пользователя из JWT."""  # (я добавил)

    if not creds:
        raise HTTPException(status_code=401, detail="Не авторизован")

    try:
        payload = jwt.decode(
            creds.credentials,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Не авторизован")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")

    res = await db.execute(select(User).where(User.id == int(user_id)))
    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    return user


async def admin_required(user: User = Depends(get_current_user)) -> User:
    """Проверка прав администратора."""  # (я добавил)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return user
