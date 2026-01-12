# backend/alembic/versions/40c886012c21_update_user_model.py
# Назначение: добавление полей name и phone в таблицу users

"""update user model

Revision ID: 40c886012c21
Revises: 5c8390c7eb7a
Create Date: 2026-01-12 18:52:32.733668
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "40c886012c21"
down_revision: Union[str, Sequence[str], None] = "5c8390c7eb7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Добавляет поля name и phone в таблицу users.
    Другие таблицы и ограничения НЕ затрагиваются.
    """
    op.add_column(
        "users",
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=False,
            server_default="",
        ),
    )


def downgrade() -> None:
    """Downgrade schema.

    Удаляет поля name и phone из таблицы users.
    """
    op.drop_column("users", "phone")
    op.drop_column("users", "name")
