# backend/alembic/versions/a63e8b75a689_add_guest_fields_to_booking.py
# Назначение: хранение данных гостя в бронировании

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a63e8b75a689"
down_revision: Union[str, Sequence[str], None] = "8a8e770ac1ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "bookings",
        sa.Column(
            "guest_name",
            sa.String(length=100),
            nullable=True,
        ),
    )  # (я добавил)

    op.add_column(
        "bookings",
        sa.Column(
            "guest_phone",
            sa.String(length=20),
            nullable=True,
        ),
    )  # (я добавил)

    op.add_column(
        "bookings",
        sa.Column(
            "guest_email",
            sa.String(length=255),
            nullable=True,
        ),
    )  # (я добавил)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("bookings", "guest_email")  # (я добавил)
    op.drop_column("bookings", "guest_phone")  # (я добавил)
    op.drop_column("bookings", "guest_name")   # (я добавил)
