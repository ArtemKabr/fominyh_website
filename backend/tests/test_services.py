# backend/tests/test_services.py — тесты услуг
# Назначение: создание и получение услуг с обязательными slug/category

import pytest


@pytest.mark.asyncio
async def test_create_service(client):
    r = await client.post(
        "/api/services",
        json={
            "name": "Массаж лица",
            "price": 3000,
            "duration_minutes": 60,
            "slug": "massage-face",  # (я добавил)
            "category": "face",      # (я добавил)
        },
    )
    assert r.status_code == 201
    assert r.json()["name"] == "Массаж лица"


@pytest.mark.asyncio
async def test_list_services(client):
    r = await client.get("/api/services")
    assert r.status_code == 200
    assert len(r.json()) >= 1
