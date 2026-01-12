"""add confirmed booking status

Revision ID: 43d8565f965d
Revises: 9f2428f77b29
Create Date: 2026-01-08 21:10:08.843592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43d8565f965d'
down_revision: Union[str, Sequence[str], None] = '9f2428f77b29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
