# backend/tests/test_admin_auth.py — тесты логина и ролей

import pytest


@pytest.mark.asyncio
async def test_admin_login_ok(async_client, admin_user):
    """Администратор может залогиниться."""  # (я добавил)
    resp = await async_client.post(
        "/api/auth/login",
        json={
            "email": admin_user.email,        # (я изменил)
            "password": "admin_password",
        },
    )
    assert resp.status_code == 200

    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login_ok(async_client, regular_user):
    """Обычный пользователь может залогиниться, но не админ."""  # (я добавил)
    resp = await async_client.post(
        "/api/auth/login",
        json={
            "email": regular_user.email,      # (я изменил)
            "password": "user_password",
        },
    )
    assert resp.status_code == 200

    data = resp.json()
    assert "access_token" in data
