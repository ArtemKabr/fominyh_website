# backend/app/schemas/salon_settings.py — схемы настроек салона

from pydantic import BaseModel, Field


class SalonSettingsOut(BaseModel):
    work_start_hour: int
    work_end_hour: int
    slot_minutes: int

    class Config:
        from_attributes = True


class SalonSettingsUpdate(BaseModel):
    work_start_hour: int = Field(..., ge=0, le=23)
    work_end_hour: int = Field(..., ge=1, le=24)
    slot_minutes: int = Field(..., gt=0)
