"""add unique constraint to expression_images

Revision ID: eb34a2cd7fa7
Revises: 1221de42cb3a
Create Date: 2026-03-28 17:31:44.770245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb34a2cd7fa7'
down_revision: Union[str, Sequence[str], None] = '1221de42cb3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ✅ 加上唯一性限制
    op.create_unique_constraint(
        "uix_type_stage", "expression_images", ["type_id", "stage"]
    )

def downgrade():
    # ✅ 移除唯一性限制
    op.drop_constraint("uix_type_stage", "expression_images", type_="unique")

