"""add user_id to bookings

Revision ID: 2c3e30f89566
Revises: ab5daac5ef0e
Create Date: 2026-01-02 19:56:52.492720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c3e30f89566'
down_revision: Union[str, Sequence[str], None] = 'ab5daac5ef0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
