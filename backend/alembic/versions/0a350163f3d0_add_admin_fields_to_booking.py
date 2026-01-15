"""add admin fields to booking

Revision ID: 0a350163f3d0
Revises: a63e8b75a689
Create Date: 2026-01-15 00:03:32.792691
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0a350163f3d0"
down_revision: Union[str, Sequence[str], None] = "a63e8b75a689"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "bookings",
        sa.Column(
            "created_by_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )  # (я добавил)

    op.add_column(
        "bookings",
        sa.Column(
            "admin_comment",
            sa.String(length=255),
            nullable=True,
        ),
    )  # (я добавил)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("bookings", "admin_comment")  # (я добавил)
    op.drop_column("bookings", "created_by_admin")  # (я добавил)
