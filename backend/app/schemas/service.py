# backend/app/schemas/service.py — схемы услуг (совместимость с тестами)

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    """Базовые поля услуги."""  # (я добавил)

    name: str
    price: int
    duration_minutes: int = Field(..., ge=1)  # (я добавил)


class ServiceCreate(ServiceBase):
    """Создание услуги."""  # (я добавил)

    model_config = ConfigDict(extra="forbid")  # (я добавил)


class ServiceRead(ServiceBase):
    """Чтение услуги."""  # (я добавил)

    id: int

    model_config = ConfigDict(from_attributes=True)  # (я добавил)
