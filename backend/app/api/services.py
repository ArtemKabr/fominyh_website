# backend/app/api/services.py — эндпоинты услуг
# Назначение: публичное API услуг

from fastapi import APIRouter, Depends, status, HTTPException  # (я добавил)
from sqlalchemy.ext.asyncio import AsyncSession
import json  # (я добавил)

from app.core.database import get_async_session
from app.schemas.service import ServiceCreate, ServiceRead
from app.services.service import (
    get_services,
    create_service,
    get_service_by_slug,  # (я добавил)
)
from app.core.redis import redis  # (я добавил)

router = APIRouter(
    prefix="/api/services",
    tags=["Services"],
)


@router.get(
    "",
    response_model=list[ServiceRead],
)
async def list_services(
    db: AsyncSession = Depends(get_async_session),
):
    """Список услуг."""  # (я добавил)

    cache_key = "services:list"  # (я добавил)
    cached = await redis.get(cache_key)  # (я добавил)

    if cached:
        return json.loads(cached)  # (я добавил)

    services = await get_services(db)
    data = [ServiceRead.model_validate(s).model_dump() for s in services]  # (я добавил)

    await redis.set(cache_key, json.dumps(data), ex=300)  # 5 минут (я добавил)
    return data


@router.get(
    "/slug/{slug}",
    response_model=ServiceRead,
)
async def get_service_by_slug_api(
    slug: str,
    db: AsyncSession = Depends(get_async_session),
) -> ServiceRead:
    """Получить услугу по slug."""  # (я добавил)

    service = await get_service_by_slug(db, slug)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )
    return ServiceRead.model_validate(service)  # (я добавил)


@router.post(
    "",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_async_session),
) -> ServiceRead:
    """Создание услуги."""  # (я добавил)
    return await create_service(db, service_in)
