from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health():
    return {"status": "ok"}
