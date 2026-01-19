# backend/app/api/services.py — эндпоинты услуг
# Назначение: публичное API услуг (список + получение по slug)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.database import get_async_session
from app.schemas.service import ServiceCreate, ServiceRead
from app.services.service import (
    get_services,
    create_service,
    get_service_by_slug,
)
from app.core.redis import redis
from app.services.services_marketing import load_services_marketing

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
) -> list[ServiceRead]:
    """Список услуг."""

    cache_key = "services:list"
    cached = await redis.get(cache_key)

    if cached:
        return json.loads(cached)

    services = await get_services(db)

    data = [
        ServiceRead.model_validate(service).model_dump()
        for service in services
    ]

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

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )

    return ServiceRead.model_validate(service)


@router.get("/marketing")
def get_services_marketing():
    """Маркетинговые описания услуг."""  # (я добавил)
    return load_services_marketing()


@router.get(
    "/{slug}",
    response_model=ServiceRead,
)
async def get_service_by_slug_api_alias(
    slug: str,
    db: AsyncSession = Depends(get_async_session),
) -> ServiceRead:
    """
    Alias для фронта.
    Позволяет обращаться /api/services/{slug}
    """  # (я добавил)

    service = await get_service_by_slug(db, slug)

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )

    return ServiceRead.model_validate(service)


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

    service = await create_service(db, service_in)

    # сбрасываем кеш списка услуг (я добавил)
    await redis.delete("services:list")

    return ServiceRead.model_validate(service)
