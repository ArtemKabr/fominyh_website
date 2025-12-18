# backend/app/api/services.py — эндпоинты услуг

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.service import ServiceCreate, ServiceRead
from app.services.service import get_services, create_service

router = APIRouter(prefix="/api/services", tags=["Services"])


@router.get(
    "",
    response_model=list[ServiceRead],
)
async def list_services(db: AsyncSession = Depends(get_db)):
    """Список услуг."""  # (я добавил)
    return await get_services(db)


@router.post(
    "",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создание услуги."""  # (я добавил)
    return await create_service(db, service_in)
