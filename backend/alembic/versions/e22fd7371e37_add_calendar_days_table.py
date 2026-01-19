"""add calendar_days table

Revision ID: e22fd7371e37
Revises: 606ab43723c2
Create Date: 2026-01-17 20:16:22.719637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e22fd7371e37'
down_revision: Union[str, Sequence[str], None] = '606ab43723c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "calendar_days",
        sa.Column("day", sa.Date(), primary_key=True),
        sa.Column(
            "is_working",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("work_start_hour", sa.Integer(), nullable=True),
        sa.Column("work_end_hour", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("calendar_days")
