# backend/app/main.py — точка входа FastAPI
# Назначение: инициализация приложения, Swagger и корректный shutdown БД

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi  #

from app.core.config import settings
from app.core.database import shutdown_engine
from app.api.services import router as services_router
from app.api.booking import router as booking_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.admin_settings import router as admin_settings_router
from app.startup import init_services_if_empty


app = FastAPI(
    title=settings.app_name,
    description=(
        "Авторизация:\n\n"
        "В Swagger в поле **Authorize** вставляется **ТОЛЬКО JWT-токен**, "
        "**без `Bearer`**.\n\n"
        "Пример:\n"
        "`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`"
    ),
)


def custom_openapi():
    """Swagger с HTTP Bearer JWT."""  #
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Вставлять ТОЛЬКО JWT, без Bearer",  #
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  #


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


@app.on_event("startup")
async def on_startup():
    """Автоинициализация данных."""  # (я добавил)
    await init_services_if_empty()  # (я добавил)