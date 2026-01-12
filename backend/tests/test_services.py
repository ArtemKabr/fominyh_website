# backend/tests/test_services.py — тесты услуг
import pytest


@pytest.mark.asyncio
async def test_create_service(client):
    r = await client.post(
        "/api/services",
        json={
            "name": "Массаж лица",
            "price": 3000,
            "duration_minutes": 60,
        },
    )
    assert r.status_code == 201
    assert r.json()["name"] == "Массаж лица"


@pytest.mark.asyncio
async def test_list_services(client):
    r = await client.get("/api/services")
    assert r.status_code == 200
    assert len(r.json()) >= 1
