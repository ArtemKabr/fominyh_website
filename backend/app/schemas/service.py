# backend/app/schemas/service.py — pydantic-схемы услуг

from pydantic import BaseModel


class ServiceBase(BaseModel):
    """Базовая схема услуги."""  # (я добавил)

    name: str
    price: int
    duration_minutes: int


class ServiceCreate(ServiceBase):
    """Схема создания услуги."""  # (я добавил)
    pass


class ServiceRead(ServiceBase):
    """Схема чтения услуги."""  # (я добавил)

    id: int

    class Config:
        from_attributes = True
