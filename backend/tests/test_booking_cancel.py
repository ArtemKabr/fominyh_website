# backend/tests/test_booking_cancel.py — отмена записи

from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_cancel_booking(client):
    """Отмена записи освобождает слот."""  # (я добавил)

    service_resp = await client.post(
        "/api/services",
        json={
            "name": "Cancel test",
            "price": 1000,
            "duration_minutes": 60,
        },
    )
    service_id = service_resp.json()["id"]

    start_dt = datetime.now() + timedelta(hours=4)
    start_time = start_dt.isoformat()

    booking_resp = await client.post(
        "/api/booking",
        json={
            "service_id": service_id,
            "start_time": start_time,
            "user_name": "Ivan",
            "phone": "+79992222222",
            "email": "b@b.ru",
        },
    )
    booking_id = booking_resp.json()["id"]

    cancel_resp = await client.post(f"/api/booking/{booking_id}/cancel")
    assert cancel_resp.status_code == 200

    free_resp = await client.get(
        "/api/booking/free",
        params={
            "day": start_dt.date().isoformat(),
            "service_id": service_id,
        },
    )

    slots = free_resp.json()["slots"]

    # сравниваем корректно: datetime -> iso без секунд
    expected_prefix = start_dt.replace(second=0, microsecond=0).isoformat()[:16]
    assert any(slot.startswith(expected_prefix) for slot in slots)
