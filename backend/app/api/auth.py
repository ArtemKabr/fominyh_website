# backend/app/api/auth.py — простая авторизация
# Назначение: регистрация и логин без JWT

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.passwords import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterIn, LoginIn  # (я использую существующие)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterIn,
    db: AsyncSession = Depends(get_async_session),
):
    """Регистрация пользователя."""

    if not data.name or not data.phone:  # (я добавил)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="name и phone обязательны",
        )

    res = await db.execute(select(User).where(User.email == data.email))
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже существует",
        )

    user = User(
        name=data.name,
        phone=data.phone,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
    }


@router.post("/login")
async def login(
    data: LoginIn,
    db: AsyncSession = Depends(get_async_session),
):
    """Логин пользователя."""

    res = await db.execute(select(User).where(User.email == data.email))
    user = res.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "is_admin": user.is_admin,
    }
