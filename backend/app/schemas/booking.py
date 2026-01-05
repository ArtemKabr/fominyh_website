# backend/app/schemas/booking.py — pydantic-схемы записи

from datetime import date, datetime
from pydantic import BaseModel, Field


class FreeSlotsQuery(BaseModel):
    """Параметры запроса свободных слотов."""

    day: date
    service_id: int | None = None


class BookingCreate(BaseModel):
    """Схема создания записи клиента."""

    service_id: int
    start_time: datetime

    user_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=20)
    email: str | None = Field(default=None, max_length=255)


class BookingRead(BaseModel):
    """Схема чтения записи."""

    id: int
    user_id: int
    service_id: int
    start_time: datetime = Field(alias="start_at")  # (я добавил)

    class Config:
        from_attributes = True  # (я добавил)
        populate_by_name = True  # (я добавил)
