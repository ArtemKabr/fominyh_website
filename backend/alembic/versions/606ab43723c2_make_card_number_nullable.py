"""make card_number nullable

Revision ID: 606ab43723c2
Revises: 39696ebe0307
Create Date: 2026-01-15 18:01:21.717280

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "606ab43723c2"
down_revision: Union[str, Sequence[str], None] = "39696ebe0307"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Сделать card_number nullable."""  # (я добавил)
    op.alter_column(
        "users",
        "card_number",
        existing_type=sa.String(length=20),
        nullable=True,
    )


def downgrade() -> None:
    """Вернуть card_number NOT NULL."""  # (я добавил)
    op.alter_column(
        "users",
        "card_number",
        existing_type=sa.String(length=20),
        nullable=False,
    )
