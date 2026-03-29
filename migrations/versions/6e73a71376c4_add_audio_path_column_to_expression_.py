"""add audio_path column to expression_images

Revision ID: 6e73a71376c4
Revises: eb34a2cd7fa7
Create Date: 2026-03-28 17:40:45.236901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e73a71376c4'
down_revision: Union[str, Sequence[str], None] = 'eb34a2cd7fa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('expression_images', sa.Column('audio_path', sa.String(length=200), nullable=True))

def downgrade():
    op.drop_column('expression_images', 'audio_path')
