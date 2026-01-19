"""add guest_comment to bookings

Revision ID: fe9fc12561ea
Revises: e22fd7371e37
Create Date: 2026-01-17 17:30:32.888864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe9fc12561ea'
down_revision: Union[str, Sequence[str], None] = 'e22fd7371e37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "bookings",
        sa.Column(
            "guest_comment",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("bookings", "guest_comment")

