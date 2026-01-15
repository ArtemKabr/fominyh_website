# backend/app/scripts/load_services.py — загрузка услуг из JSON в БД
# Назначение: первичное наполнение таблицы services из services_db.json

import json
import asyncio
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import get_engine, Base
from app.models.service import Service


DATA_FILE = Path(__file__).parent.parent / "data" / "services_db.json"


async def load_services() -> None:
    """Загрузить услуги из services_db.json в БД."""  # (я добавил)

    engine = get_engine()

    # 1. Создаём таблицы, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # (я добавил)

    # 2. Создаём async-сессию
    async_session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        # 3. Проверка: если услуги уже есть — выходим
        res = await session.execute(select(Service.id))
        if res.first():
            print("Услуги уже существуют, загрузка не требуется")  # (я добавил)
            return

        # 4. Читаем JSON
        with DATA_FILE.open(encoding="utf-8") as f:
            services = json.load(f)

        # 5. Загружаем услуги (ВСЕ обязательные поля)
        for item in services:
            service = Service(
                name=item["name"],
                slug=item["slug"],  # (я добавил)
                category=item.get("category"),  # (я добавил)
                description=item.get("description"),  # (я добавил)
                image=item.get("image"),  # (я добавил)
                price=item["price"],
                duration_minutes=item["duration_minutes"],
            )
            session.add(service)

        await session.commit()
        print(f"Загружено услуг: {len(services)}")  # (я добавил)


if __name__ == "__main__":
    asyncio.run(load_services())
