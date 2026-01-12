# backend/app/api/admin.py — админка без JWT

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


async def get_admin(user_id: int, db: AsyncSession) -> User:
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return user
