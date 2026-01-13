"""add category image benefits to services

Revision ID: 5c8390c7eb7a
Revises: cbc3cdc68b3c
Create Date: 2026-01-12 17:59:38
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5c8390c7eb7a"
down_revision: Union[str, Sequence[str], None] = "cbc3cdc68b3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. category — добавляем временно nullable
    op.add_column(
        "services",
        sa.Column("category", sa.String(length=50), nullable=True),
    )

    # 2. image
    op.add_column(
        "services",
        sa.Column("image", sa.String(length=255), nullable=True),
    )

    # 3. benefits
    op.add_column(
        "services",
        sa.Column("benefits", sa.JSON(), nullable=True),
    )

    # 4. проставляем дефолтную категорию для существующих услуг
    op.execute("UPDATE services SET category = 'other' WHERE category IS NULL")

    # 5. делаем category обязательным
    op.alter_column(
        "services",
        "category",
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("services", "benefits")
    op.drop_column("services", "image")
    op.drop_column("services", "category")
