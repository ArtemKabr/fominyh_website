# backend/app/main.py — точка входа FastAPI
# Назначение: инициализация приложения и корректный shutdown БД

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import shutdown_engine
from app.api.services import router as services_router
from app.api.booking import router as booking_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.admin_settings import router as admin_settings_router

app = FastAPI(title=settings.app_name)

app.include_router(services_router)
app.include_router(booking_router)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(admin_settings_router)


@app.on_event("shutdown")
async def on_shutdown():
    """Корректное закрытие engine БД."""
    await shutdown_engine()


@app.get("/health")
def health():
    return {"status": "ok"}
