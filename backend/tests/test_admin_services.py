# backend/tests/test_admin_services.py — доступ к админ-роутам услуг
# проверка: без токена / user / admin

import pytest


@pytest.mark.asyncio
async def test_admin_services_requires_token(async_client):
    """Без токена доступ запрещён."""  # (я добавил)
    resp = await async_client.post(
        "/api/admin/services",
        json={"name": "X", "price": 1, "duration_minutes": 30},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_admin_services_user_forbidden(async_client, user_token):
    """Обычный пользователь не имеет доступа."""  # (я добавил)
    resp = await async_client.post(
        "/api/admin/services",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "X", "price": 1, "duration_minutes": 30},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_admin_services_admin_ok(async_client, admin_token):
    """Администратор может создавать услуги."""  # (я добавил)
    resp = await async_client.post(
        "/api/admin/services",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "X", "price": 1, "duration_minutes": 30},
    )
    assert resp.status_code in (200, 201)
