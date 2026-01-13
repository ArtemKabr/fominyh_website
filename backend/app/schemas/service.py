# backend/app/schemas/service.py — схемы услуг (совместимость с тестами)

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    """Базовые поля услуги."""  # 

    name: str
    price: int
    duration_minutes: int = Field(..., ge=1)  # 


class ServiceCreate(ServiceBase):
    """Создание услуги."""  # 

    model_config = ConfigDict(extra="forbid")  # 


class ServiceRead(ServiceBase):
    """Чтение услуги."""  # 

    id: int

    model_config = ConfigDict(from_attributes=True)  # 
