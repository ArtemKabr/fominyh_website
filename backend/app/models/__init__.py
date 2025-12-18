# backend/app/models/__init__.py — регистрация моделей

from app.models.user import User  # (я добавил)
from app.models.service import Service  # (я добавил)
from app.models.booking import Booking  # (я добавил)

__all__ = ["User", "Service", "Booking"]
