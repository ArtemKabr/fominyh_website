# backend/alembic/versions/0cb5d6658e52_add_booking_status.py
# миграция: безопасное добавление статуса записи

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0cb5d6658e52"
down_revision: Union[str, Sequence[str], None] = "3053bbff7929"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавление статуса записи."""  # (я добавил)
    # 1. Добавляем колонку с server_default  # (я добавил)
    op.add_column(
        "bookings",
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="planned",  # (я добавил)
            nullable=False,
        ),
    )

    # 2. Убираем server_default (best practice)  # (я добавил)
    op.alter_column(
        "bookings",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    """Удаление статуса записи."""  # (я добавил)
    op.drop_column("bookings", "status")
