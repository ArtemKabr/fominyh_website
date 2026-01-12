"""add is_verified to users

Revision ID: ba13288bac6f
Revises: 9f6aafaa18eb
Create Date: 2026-01-07 15:25:26.908871
"""
# backend/alembic/versions/ba13288bac6f_add_is_verified_to_users.py
# Назначение: добавить флаг подтверждения email пользователю

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ba13288bac6f"
down_revision: Union[str, Sequence[str], None] = "9f6aafaa18eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),  # 
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_verified")
