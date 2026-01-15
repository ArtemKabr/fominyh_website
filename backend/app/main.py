# backend/app/main.py — точка входа FastAPI
# Назначение: инициализация приложения, Swagger под логин/пароль (без JWT)

import os  # (я добавил)

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import shutdown_engine
from app.api.services import router as services_router
from app.api.booking import router as booking_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.admin_settings import router as admin_settings_router
from app.api.user import router as user_router
from app.startup import init_services_if_empty
from app.api.reserve import router as reserve_router


# --------------------
# Инициализация media
# --------------------
os.makedirs("media/avatars", exist_ok=True)  # (я добавил)


app = FastAPI(
    title=settings.app_name,
    description=(
        "Авторизация в системе:\n\n"
        "1. Выполните **POST /api/auth/login** с email и паролем.\n"
        "2. В ответе получите **user_id**.\n"
        "3. Для всех защищённых эндпоинтов (особенно `/api/admin/*`) "
        "передавайте заголовок:\n\n"
        "**X-User-Id: <user_id>**\n\n"
        "JWT и Bearer НЕ используются."
    ),
)


def custom_openapi():
    """
    Swagger БЕЗ JWT.
    Используется кастомный заголовок X-User-Id.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    # --- ОПИСАНИЕ кастомной авторизации ---
    openapi_schema.setdefault("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "XUserIdAuth": {  # (я добавил)
            "type": "apiKey",
            "in": "header",
            "name": "X-User-Id",
            "description": (
                "Авторизация по user_id.\n\n"
                "Получите user_id через /api/auth/login "
                "и передавайте его в заголовке X-User-Id."
            ),
        }
    }

    # --- Применяем ТОЛЬКО к защищённым роутам ---
    openapi_schema["security"] = [{"XUserIdAuth": []}]  # (я добавил)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# --------------------
# Роутеры
# --------------------
app.include_router(services_router)
app.include_router(booking_router)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(admin_settings_router)
app.include_router(user_router)
app.include_router(reserve_router)


# --------------------
# Static files
# --------------------
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.on_event("shutdown")
async def on_shutdown():
    """Корректное закрытие engine БД."""
    await shutdown_engine()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    """Автоинициализация данных."""
    await init_services_if_empty()
