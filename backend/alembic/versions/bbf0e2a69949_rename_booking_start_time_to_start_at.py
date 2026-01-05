# backend/alembic/versions/bbf0e2a69949_rename_booking_start_time_to_start_at.py
# безопасное переименование start_time -> start_at

"""rename booking start_time to start_at

Revision ID: bbf0e2a69949
Revises: 18fb1350f9aa
Create Date: 2026-01-04 14:38:50.063569
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = "bbf0e2a69949"
down_revision = "18fb1350f9aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str) -> bool:
    """Проверка существования колонки."""
    conn = op.get_bind()
    result = conn.execute(
        text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = :table
              AND column_name = :column
            """
        ),
        {"table": table, "column": column},
    )
    return result.first() is not None


def upgrade() -> None:
    """Переименовать start_time в start_at (если ещё не переименовано)."""
    if _column_exists("bookings", "start_time"):
        op.alter_column(
            "bookings",
            "start_time",
            new_column_name="start_at",
            existing_type=sa.DateTime(),
            existing_nullable=False,
        )


def downgrade() -> None:
    """Вернуть start_at в start_time (если существует)."""
    if _column_exists("bookings", "start_at"):
        op.alter_column(
            "bookings",
            "start_at",
            new_column_name="start_time",
            existing_type=sa.DateTime(),
            existing_nullable=False,
        )
