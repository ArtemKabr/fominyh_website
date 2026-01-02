# backend/app/schemas/service.py — pydantic-схемы услуг

from pydantic import BaseModel


class ServiceBase(BaseModel):
    """Базовая схема услуги."""

    name: str
    price: int
    duration_minutes: int


class ServiceCreate(ServiceBase):
    """Схема создания услуги."""
    pass


class ServiceRead(ServiceBase):
    """Схема чтения услуги."""

    id: int

    class Config:
        from_attributes = True
