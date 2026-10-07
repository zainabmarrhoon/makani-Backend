"""add store builder settings

Revision ID: 3abd25260121
Revises: 162e2774d0a2
Create Date: 2026-10-07 11:53:00.281337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3abd25260121'
down_revision: Union[str, Sequence[str], None] = '162e2774d0a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'stores',
        sa.Column(
            'show_home',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'show_products',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'show_about',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'show_contact',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'show_cart',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'show_orders',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'hero_title',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'hero_description',
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'hero_button_text',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'hero_image',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'about_title',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'about_description',
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        'stores',
        sa.Column(
            'benefitpay_iban',
            sa.String(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('stores', 'benefitpay_iban')
    op.drop_column('stores', 'about_description')
    op.drop_column('stores', 'about_title')
    op.drop_column('stores', 'hero_image')
    op.drop_column('stores', 'hero_button_text')
    op.drop_column('stores', 'hero_description')
    op.drop_column('stores', 'hero_title')
    op.drop_column('stores', 'show_orders')
    op.drop_column('stores', 'show_cart')
    op.drop_column('stores', 'show_contact')
    op.drop_column('stores', 'show_about')
    op.drop_column('stores', 'show_products')
    op.drop_column('stores', 'show_home')