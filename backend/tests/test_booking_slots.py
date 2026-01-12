# backend/tests/test_booking_slots.py — слоты записи
from datetime import date
import pytest


@pytest.mark.asyncio
async def test_get_free_slots(client):
    r = await client.get(
        "/api/booking/free",
        params={"day": date.today().isoformat(), "service_id": 1},
    )
    assert r.status_code == 200
    assert "slots" in r.json()
    assert isinstance(r.json()["slots"], list)
