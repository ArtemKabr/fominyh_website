# backend/app/models/__init__.py — регистрация моделей

from .user import User  # noqa
from .service import Service  # noqa
from .booking import Booking  # noqa


__all__ = ["User", "Service", "Booking"]
