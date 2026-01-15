# backend/app/api/reserve.py — API резерва
# Назначение: публичное создание резерва

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.reserve import Reserve
from app.schemas.reserve import ReserveCreate, ReserveOut

router = APIRouter(prefix="/api/reserve", tags=["Reserve"])


@router.post("", response_model=ReserveOut)
async def create_reserve(
    payload: ReserveCreate,
    db: AsyncSession = Depends(get_async_session),
):
    """Создать резерв на день (когда нет слотов)."""

    reserve = Reserve(**payload.model_dump())
    db.add(reserve)
    await db.commit()
    await db.refresh(reserve)

    return reserve
