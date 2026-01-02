# backend/app/services/service.py — бизнес-логика услуг

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.service import Service
from app.schemas.service import ServiceCreate


async def get_services(db: AsyncSession) -> list[Service]:
    """Получить список всех услуг."""
    result = await db.execute(
        select(Service).order_by(Service.id)
    )
    return result.scalars().all()


async def create_service(
    db: AsyncSession,
    service_in: ServiceCreate,
) -> Service:
    """Создать новую услугу."""
    service = Service(**service_in.model_dump())
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service
