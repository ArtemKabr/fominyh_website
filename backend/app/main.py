from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine

app = FastAPI(title=settings.APP_NAME)


@app.get("/health")
def health():
    return {"status": "ok"}
