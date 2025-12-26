# backend/tests/test_booking_double.py — защита от двойной записи

from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_double_booking_not_allowed(client):
    """Нельзя создать две записи на один слот."""  # (я добавил)

    service_resp = await client.post(
        "/api/services",
        json={
            "name": "Double test",
            "price": 1000,
            "duration_minutes": 60,
        },
    )
    service_id = service_resp.json()["id"]

    start_time = (datetime.now() + timedelta(hours=3)).isoformat()

    payload = {
        "service_id": service_id,
        "start_time": start_time,
        "user_name": "Ivan",
        "phone": "+79991111111",
        "email": "a@a.ru",
    }

    first = await client.post("/api/booking", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/booking", json=payload)
    assert second.status_code == 409
