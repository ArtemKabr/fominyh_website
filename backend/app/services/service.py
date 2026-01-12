# backend/app/services/service.py — бизнес-логика услуг
# Назначение: получение и создание услуг

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.service import Service
from app.schemas.service import ServiceCreate


def _make_slug(name: str) -> str:
    """Простой slug из названия услуги."""  # (я добавил)
    return name.strip().lower().replace(" ", "-").replace("_", "-")


async def get_services(db: AsyncSession) -> list[Service]:
    """Получить список всех реальных услуг."""  # (я добавил)
    result = await db.execute(
        select(Service)
        .where(Service.category != "other")  # (я добавил)
        .order_by(Service.id)
    )
    return result.scalars().all()


async def get_service_by_slug(
    db: AsyncSession,
    slug: str,
) -> Service | None:
    """Получить услугу по slug."""
    result = await db.execute(select(Service).where(Service.slug == slug))
    return result.scalar_one_or_none()


async def create_service(
    db: AsyncSession,
    service_in: ServiceCreate,
) -> Service:
    """Создать новую услугу."""
    data = service_in.model_dump()

    if not data.get("slug"):  # (я добавил)
        data["slug"] = _make_slug(data["name"])  # (я добавил)

    if not data.get("category"):  # (я добавил)
        data["category"] = "face"  # (я добавил)

    service = Service(**data)
    db.add(service)
    await db.commit()
    await db.refresh(service)

    return service
