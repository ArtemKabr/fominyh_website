# backend/app/schemas/schedule.py — схемы расписания
from datetime import datetime
from pydantic import BaseModel


class FreeSlot(BaseModel):
    """Свободный временной слот."""

    start_time: datetime
    end_time: datetime
