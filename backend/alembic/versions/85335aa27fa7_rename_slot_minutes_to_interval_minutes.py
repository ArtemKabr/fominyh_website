# backend/alembic/versions/xxxx_rename_slot_minutes.py
# Назначение: приведение salon_settings к актуальной модели

from alembic import op


revision = "85335aa27fa7"
down_revision = "bbf0e2a69949"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "salon_settings",
        "slot_minutes",
        new_column_name="interval_minutes",
    )


def downgrade() -> None:
    op.alter_column(
        "salon_settings",
        "interval_minutes",
        new_column_name="slot_minutes",
    )
