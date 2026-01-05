# backend/alembic/versions/2c3e30f89566_add_user_id_to_bookings.py
# — техническая миграция (user_id уже существует)

"""add user_id to bookings

Revision ID: 2c3e30f89566
Revises: ab5daac5ef0e
Create Date: 2026-01-02 19:56:52.492720
"""
from typing import Sequence, Union


revision: str = "2c3e30f89566"
down_revision = "8db48134ba7d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """user_id уже добавлен в initial schema."""
    pass


def downgrade() -> None:
    """Откат не требуется."""
    pass
