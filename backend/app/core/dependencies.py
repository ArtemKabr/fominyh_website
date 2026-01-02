# backend/app/core/dependencies.py — зависимости авторизации
# отвечает за получение текущего пользователя и проверку прав

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.models.user import User


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    """Получить текущего пользователя по JWT."""  # (я добавил)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id_raw = payload.get("sub")  # (я добавил)
        if user_id_raw is None:
            raise credentials_exception

        user_id = int(user_id_raw)  # (я добавил)

    except (JWTError, ValueError):
        raise credentials_exception  # (я добавил)

    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user


async def admin_required(
    user: User = Depends(get_current_user),
) -> User:
    """Проверка прав администратора."""  # (я добавил)

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуются права администратора",
        )

    return user
