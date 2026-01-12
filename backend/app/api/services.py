# backend/app/api/services.py — эндпоинты услуг
# Назначение: публичное API услуг

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.schemas.service import ServiceCreate, ServiceRead
from app.services.service import (
    get_services,
    create_service,
    get_service_by_slug,
)

router = APIRouter(
    prefix="/api/services",
    tags=["Services"],
)


@router.get("", response_model=list[ServiceRead])
async def list_services(
    db: AsyncSession = Depends(get_async_session),
) -> list[ServiceRead]:
    """Список услуг."""
    return await get_services(db)  # (я добавил)


@router.get(
    "/slug/{slug}",
    response_model=ServiceRead,
)
async def get_service_by_slug_api(
    slug: str,
    db: AsyncSession = Depends(get_async_session),
) -> ServiceRead:
    """Получить услугу по slug."""

    service = await get_service_by_slug(db, slug)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )
    return service


@router.post(
    "",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_async_session),
) -> ServiceRead:
    """Создание услуги."""
    return await create_service(db, service_in)
