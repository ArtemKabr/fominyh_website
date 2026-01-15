# backend/app/schemas/service.py — схемы услуг
# Назначение: вход/выход API услуг

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    """Базовые поля услуги."""  # (я добавил)

    name: str
    price: int
    duration_minutes: int = Field(..., ge=1)


class ServiceCreate(ServiceBase):
    """Создание услуги."""  # (я добавил)

    slug: str  # (я добавил)
    category: str  # (я добавил)
    description: str | None = None  # (я добавил)
    image: str | None = None  # (я добавил)
    benefits: list[str] | None = None  # (я добавил)

    model_config = ConfigDict(extra="forbid")


class ServiceRead(ServiceBase):
    """Чтение услуги."""  # (я добавил)

    id: int
    slug: str  # (я добавил)
    category: str  # (я добавил)
    description: str | None = None  # (я добавил)
    image: str | None = None  # (я добавил)
    benefits: list[str] | None = None  # (я добавил)

    model_config = ConfigDict(from_attributes=True)
