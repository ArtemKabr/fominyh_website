# backend/app/schemas/booking.py — схемы бронирования
# Назначение: схемы бронирования (строго под фронт)
from datetime import date, datetime
from pydantic import BaseModel, Field, model_validator


class FreeSlotsQuery(BaseModel):
    """Параметры запроса свободных слотов."""
    day: date
    service_id: int


class BookingCreate(BaseModel):
    """Создание записи клиента."""

    service_id: int

    day: date  # YYYY-MM-DD
    time: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}$",
        description="Время в формате HH:MM",
    )

    user_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=20)
    email: str | None = Field(default=None, max_length=255)

    start_time: datetime | None = None  # (я добавил)

    @model_validator(mode="after")
    def build_start_time(self):
        """Собираем start_time из day + time."""  # (я добавил)
        self.start_time = datetime.fromisoformat(
            f"{self.day} {self.time}"
        )
        return self


class BookingRead(BaseModel):
    """Чтение записи."""

    id: int
    service_id: int
    start_time: datetime
    status: str

    class Config:
        from_attributes = True


class AdminSlotBookIn(BaseModel):
    """Бронирование слота админом (из админки)."""  # (я добавил)

    service_id: int  # (я добавил)
    day: date  # (я добавил)
    time: str = Field(  # (я добавил)
        ...,
        pattern=r"^\d{2}:\d{2}$",
        description="Время в формате HH:MM",
    )
    mode: str = Field(  # (я добавил)
        ...,
        pattern=r"^(admin|client)$",
        description="admin = бронь админа, client = бронь за клиента",
    )
    guest_name: str | None = None  # (я добавил)
    guest_phone: str | None = None  # (я добавил)
    guest_email: str | None = None  # (я добавил)
    comment: str | None = None  # (я добавил)

    start_time: datetime | None = None  # (я добавил)

    @model_validator(mode="after")
    def build_start_time(self):
        """Собираем start_time из day + time."""  # (я добавил)
        self.start_time = datetime.fromisoformat(f"{self.day} {self.time}")
        return self
