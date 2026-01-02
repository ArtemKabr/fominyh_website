# backend/app/api/auth.py — регистрация и логин

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.passwords import hash_password, verify_password
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import RegisterIn, LoginIn, TokenOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_async_session)) -> TokenOut:
    """Регистрация пользователя."""  # (я добавил)

    res = await db.execute(select(User).where(User.email == payload.email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_admin=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=user.id)
    return TokenOut(access_token=token)


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_async_session)) -> TokenOut:
    """Логин пользователя."""  # (я добавил)

    res = await db.execute(select(User).where(User.email == payload.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    token = create_access_token(subject=user.id)
    return TokenOut(access_token=token)
