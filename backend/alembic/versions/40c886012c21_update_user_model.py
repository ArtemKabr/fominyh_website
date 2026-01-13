# backend/alembic/versions/40c886012c21_update_user_model.py
# Назначение: безопасное добавление флага администратора пользователю

"""update user model

Revision ID: 40c886012c21
Revises: 5c8390c7eb7a
Create Date: 2026-01-12 18:52:32.733668
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  #

# revision identifiers, used by Alembic.
revision: str = "40c886012c21"
down_revision: Union[str, Sequence[str], None] = "5c8390c7eb7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()  #
    inspector = inspect(bind)  #

    columns = [col["name"] for col in inspector.get_columns("users")]  #

    if "is_admin" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "is_admin",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )  #


def downgrade() -> None:
    """Откат добавления флага администратора."""
    op.drop_column("users", "is_admin")
