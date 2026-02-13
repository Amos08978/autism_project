"""add expression tables

Revision ID: 1221de42cb3a
Revises: d8b48c9c0999
Create Date: 2026-02-11 23:14:33.853493
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1221de42cb3a'
down_revision: Union[str, Sequence[str], None] = 'd8b48c9c0999'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'expression_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('type_name')
    )
    op.create_index(op.f('ix_expression_types_id'), 'expression_types', ['id'], unique=False)

    op.create_table(
        'expression_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('stage', sa.String(length=20), nullable=False),
        sa.Column('image_path', sa.String(length=200), nullable=False),
        sa.ForeignKeyConstraint(['type_id'], ['expression_types.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expression_images_id'), 'expression_images', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_expression_images_id'), table_name='expression_images')
    op.drop_table('expression_images')
    op.drop_index(op.f('ix_expression_types_id'), table_name='expression_types')
    op.drop_table('expression_types')