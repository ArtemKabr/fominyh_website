"""add bonus and discount fields to user

Revision ID: f748c23e4d3c
Revises: xxxx
Create Date: 2026-01-14 13:19:18.958949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f748c23e4d3c'
down_revision: Union[str, Sequence[str], None] = 'xxxx'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Добавить бонусы, скидку и карту пользователю."""

    op.add_column(
        "users",
        sa.Column(
            "card_number",
            sa.String(length=20),
            nullable=True,  # временно, заполним ниже (я добавил)
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "discount_percent",
            sa.Integer(),
            nullable=False,
            server_default="0",  # (я добавил)
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "bonus_balance",
            sa.Integer(),
            nullable=False,
            server_default="0",  # (я добавил)
        ),
    )

    # Заполняем номер карты для существующих пользователей
    op.execute(
        """
        UPDATE users
        SET card_number = 'CARD-' || id
        """
    )  # (я добавил)

    # Делаем поле обязательным
    op.alter_column(
        "users",
        "card_number",
        nullable=False,
    )

    # Уникальность номера карты
    op.create_unique_constraint(
        "uq_users_card_number",
        "users",
        ["card_number"],
    )


def downgrade() -> None:
    """Откат бонусов, скидки и карты."""

    op.drop_constraint(
        "uq_users_card_number",
        "users",
        type_="unique",
    )

    op.drop_column("users", "bonus_balance")
    op.drop_column("users", "discount_percent")
    op.drop_column("users", "card_number")

