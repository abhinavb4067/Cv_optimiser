"""lifetime credits for free plan

Revision ID: 4bf1d4689d10
Revises: 523ffd296cb2
Create Date: 2026-11-14 17:55:02.012448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4bf1d4689d10'
down_revision: Union[str, None] = '523ffd296cb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('subscription_plans', sa.Column('credit_reset_period', sa.String(length=20), nullable=True))
    op.add_column('subscription_plans', sa.Column('credit_limit', sa.Integer(), nullable=True))

    # Free plan becomes a one-time lifetime pool; existing monthly_credit_limit
    # becomes the new monthly credit_limit for paid plans.
    op.execute("UPDATE subscription_plans SET credit_reset_period = 'lifetime', credit_limit = 30 WHERE slug = 'free'")
    op.execute(
        "UPDATE subscription_plans SET credit_reset_period = 'monthly', credit_limit = monthly_credit_limit "
        "WHERE slug != 'free'"
    )

    op.alter_column('subscription_plans', 'credit_reset_period', nullable=False)
    op.alter_column('subscription_plans', 'credit_limit', nullable=False)

    op.drop_column('subscription_plans', 'monthly_credit_limit')
    op.drop_column('subscription_plans', 'daily_credit_limit')


def downgrade() -> None:
    op.add_column('subscription_plans', sa.Column('daily_credit_limit', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('subscription_plans', sa.Column('monthly_credit_limit', sa.INTEGER(), autoincrement=False, nullable=True))

    op.execute("UPDATE subscription_plans SET daily_credit_limit = 5, monthly_credit_limit = credit_limit WHERE slug = 'free'")
    op.execute("UPDATE subscription_plans SET daily_credit_limit = credit_limit / 12, monthly_credit_limit = credit_limit WHERE slug != 'free'")

    op.alter_column('subscription_plans', 'daily_credit_limit', nullable=False)
    op.alter_column('subscription_plans', 'monthly_credit_limit', nullable=False)

    op.drop_column('subscription_plans', 'credit_limit')
    op.drop_column('subscription_plans', 'credit_reset_period')
