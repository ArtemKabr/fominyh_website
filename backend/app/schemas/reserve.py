# backend/app/schemas/reserve.py — схемы резерва
# Назначение: входные/выходные данные резерва

from datetime import date
from pydantic import BaseModel, Field


class ReserveCreate(BaseModel):
    service_id: int
    day: date
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=5, max_length=20)
    email: str | None = None
    comment: str | None = None


class ReserveOut(BaseModel):
    id: int
    service_id: int
    day: date
    name: str
    phone: str
    email: str | None
    comment: str | None

    class Config:
        from_attributes = True
