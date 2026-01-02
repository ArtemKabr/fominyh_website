# backend/alembic/versions/18fb1350f9aa_add_salon_settings.py
"""add salon settings

Revision ID: 18fb1350f9aa
Revises: XXXX
Create Date: 2026-01-xx
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "18fb1350f9aa"
down_revision = "XXXX"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Добавить настройки салона."""
    op.create_table(
        "salon_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("work_start_hour", sa.Integer(), nullable=False),
        sa.Column("work_end_hour", sa.Integer(), nullable=False),
        sa.Column("interval_minutes", sa.Integer(), nullable=False),
    )

    # одна строка настроек по умолчанию
    op.execute(
        """
        INSERT INTO salon_settings (id, work_start_hour, work_end_hour, interval_minutes)
        VALUES (1, 9, 21, 30)
        """
    )


def downgrade() -> None:
    """Удалить настройки салона."""
    op.drop_table("salon_settings")
