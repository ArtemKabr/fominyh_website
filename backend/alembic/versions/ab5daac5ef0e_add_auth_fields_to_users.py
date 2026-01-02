"""add auth fields to users

Revision ID: ab5daac5ef0e
Revises: 8db48134ba7d
Create Date: 2026-01-02 22:16:38.092298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab5daac5ef0e'
down_revision: Union[str, Sequence[str], None] = '8db48134ba7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
