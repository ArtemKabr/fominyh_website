# backend/alembic/versions/ab5daac5ef0e_add_auth_fields_to_users.py
# — добавление auth-полей в users

"""add auth fields to users

Revision ID: ab5daac5ef0e
Revises: 8db48134ba7d
Create Date: 2026-01-02 22:16:38.092298
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision = "ab5daac5ef0e"
down_revision = "85335aa27fa7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Добавить auth-поля пользователю."""
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True),  # (я добавил)
    )
    op.add_column(
        "users",
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),  # (я добавил)
    )


def downgrade() -> None:
    """Удалить auth-поля."""
    op.drop_column("users", "is_admin")  # (я добавил)
    op.drop_column("users", "password_hash")  # (я добавил)
