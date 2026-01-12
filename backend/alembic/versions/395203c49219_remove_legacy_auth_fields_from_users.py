# backend/alembic/versions/xxxx_remove_legacy_auth_fields_from_users.py
# Назначение: удаление legacy-полей auth из users

"""remove legacy auth fields from users"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "xxxx"
down_revision: Union[str, Sequence[str], None] = "40c886012c21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("users", "is_verified")
    op.drop_column("users", "telegram_chat_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "telegram_chat_id",
            sa.BigInteger(),
            nullable=True,
        ),
    )
