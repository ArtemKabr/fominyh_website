"""add avatar_url to users

Revision ID: 8a8e770ac1ff
Revises: f748c23e4d3c
Create Date: 2026-01-14 15:43:15.470778
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a8e770ac1ff"
down_revision: Union[str, Sequence[str], None] = "f748c23e4d3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавление avatar_url в users."""  # (я добавил)
    op.add_column(
        "users",
        sa.Column(
            "avatar_url",
            sa.String(length=255),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Удаление avatar_url из users."""  # (я добавил)
    op.drop_column("users", "avatar_url")
