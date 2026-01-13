# backend/app/commands/load_services.py — загрузка услуг в БД
# Назначение: начальная загрузка услуг из JSON

import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service
from app.core.database import async_session_maker  # для CLI запуска

DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "services_db.json"
)  # 


async def load_services(db: AsyncSession) -> None:
    """Загрузка услуг в базу данных."""  # 

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Файл не найден: {DATA_PATH}")  # 

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    for item in data:
        # проверяем по slug, а не по id  # 
        res = await db.execute(
            select(Service).where(Service.slug == item["slug"])
        )
        exists = res.scalar_one_or_none()

        if exists:
            continue

        service = Service(
            name=item["name"],
            slug=item["slug"],
            category=item["category"],
            description=item["description"],
            price=item["price"],
            duration_minutes=item.get("duration")
            or item.get("duration_minutes"),  # 
            image=item.get("image"),
            benefits=item.get("benefits"),
        )

        db.add(service)

    await db.commit()


# --- CLI запуск (оставляем) ---

async def _run_cli() -> None:  # 
    async with async_session_maker() as session:
        await load_services(session)


if __name__ == "__main__":
    asyncio.run(_run_cli())
