# alembic/versions/XXXX_add_salon_settings_table.py
# add salon settings table

from alembic import op
import sqlalchemy as sa

revision = "XXXX"
down_revision = "2c3e30f89566"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "salon_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("work_start_hour", sa.Integer(), nullable=False),
        sa.Column("work_end_hour", sa.Integer(), nullable=False),
        sa.Column("slot_minutes", sa.Integer(), nullable=False),
    )

    op.execute(
        """
        INSERT INTO salon_settings (id, work_start_hour, work_end_hour, slot_minutes)
        VALUES (1, 10, 20, 30)
        """
    )


def downgrade() -> None:
    op.drop_table("salon_settings")
