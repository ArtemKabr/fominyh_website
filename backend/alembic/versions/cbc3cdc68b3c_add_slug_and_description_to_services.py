# backend/alembic/versions/cbc3cdc68b3c_add_slug_and_description_to_services.py
# Назначение: добавить slug и description с безопасной генерацией уникальных slug

"""add slug and description to services

Revision ID: cbc3cdc68b3c
Revises: 43d8565f965d
Create Date: 2026-01-12 17:44:03.841605
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "cbc3cdc68b3c"
down_revision: Union[str, Sequence[str], None] = "43d8565f965d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Добавляем slug временно nullable  #
    op.add_column(
        "services",
        sa.Column("slug", sa.String(length=255), nullable=True),
    )

    # 2. Добавляем description  #
    op.add_column(
        "services",
        sa.Column("description", sa.Text(), nullable=True),
    )

    # 3. Расширяем name  #
    op.alter_column(
        "services",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=255),
        existing_nullable=False,
    )

    # 4. Генерация уникальных slug для существующих записей  #
    op.execute(
        """
        WITH base AS (
            SELECT
                id,
                LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9]+', '-', 'g')) AS base_slug
            FROM services
        ),
        numbered AS (
            SELECT
                id,
                base_slug,
                ROW_NUMBER() OVER (PARTITION BY base_slug ORDER BY id) AS rn
            FROM base
        )
        UPDATE services s
        SET slug = CASE
            WHEN n.rn = 1 THEN n.base_slug
            ELSE n.base_slug || '-' || (n.rn - 1)
        END
        FROM numbered n
        WHERE s.id = n.id
        """
    )

    # 5. Делаем slug NOT NULL  #
    op.alter_column(
        "services",
        "slug",
        nullable=False,
    )

    # 6. Вешаем уникальное ограничение  #
    op.create_unique_constraint(
        "uq_services_slug",
        "services",
        ["slug"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_services_slug",
        "services",
        type_="unique",
    )

    op.alter_column(
        "services",
        "name",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )

    op.drop_column("services", "description")
    op.drop_column("services", "slug")
