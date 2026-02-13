"""create expression tables

Revision ID: 4ce257e0500c
Revises: 
Create Date: 2026-02-11 23:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ce257e0500c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 建立 expression_types 表
    op.create_table(
        'expression_types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type_name', sa.String(length=50), nullable=False, unique=True)
    )

    # 建立 expression_images 表
    op.create_table(
        'expression_images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type_id', sa.Integer, sa.ForeignKey('expression_types.id'), nullable=False),
        sa.Column('stage', sa.String(length=20), nullable=False),
        sa.Column('image_path', sa.String(length=200), nullable=False)
    )


def downgrade():
    # 回滾時刪除新表
    op.drop_table('expression_images')
    op.drop_table('expression_types')