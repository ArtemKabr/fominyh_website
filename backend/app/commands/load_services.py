# backend/app/commands/load_services.py — загрузка услуг в БД
# Назначение: начальная загрузка услуг из JSON

import asyncio
import json
from pathlib import Path

from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.service import Service

DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "services_db.json"
)  # (я добавил)


async def load_services() -> None:
    """Загрузка услуг в базу данных."""  # (я добавил)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Файл не найден: {DATA_PATH}")  # (я добавил)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    async with async_session_maker() as session:  # type: AsyncSession
        for item in data:
            # проверяем по slug, а не по id  # (я добавил)
            res = await session.execute(
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
                or item.get("duration_minutes"),  # (я добавил)
                image=item.get("image"),
                benefits=item.get("benefits"),
            )

            session.add(service)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(load_services())
