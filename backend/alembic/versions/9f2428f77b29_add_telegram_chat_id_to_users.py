"""add telegram_chat_id to users

Revision ID: 9f2428f77b29
Revises: ba13288bac6f
Create Date: 2026-01-07 18:25:51.361932
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f2428f77b29"
down_revision: Union[str, Sequence[str], None] = "ba13288bac6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавить telegram_chat_id пользователю."""  # 
    op.add_column(
        "users",
        sa.Column(
            "telegram_chat_id",
            sa.BigInteger(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Удалить telegram_chat_id у пользователя."""  # 
    op.drop_column("users", "telegram_chat_id")
