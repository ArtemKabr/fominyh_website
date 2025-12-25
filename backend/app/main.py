# backend/app/main.py — точка входа FastAPI

from fastapi import FastAPI

from app.core.config import settings
from app.api.services import router as services_router  # (я добавил)
from app.api.booking import router as booking_router  # (я добавил)


app = FastAPI(title=settings.app_name)

app.include_router(services_router)  # (я добавил)
app.include_router(booking_router)  # (я добавил)


@app.get("/health")
def health():
    return {"status": "ok"}
