"""make transaction category required

Revision ID: d9dcdfb4e1b4
Revises: ecc8a4183328
Create Date: 2026-11-05 11:13:42.087249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9dcdfb4e1b4'
down_revision: Union[str, Sequence[str], None] = 'ecc8a4183328'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'movimentacoes',
        'categoria_id',
        existing_type=sa.Integer(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'movimentacoes',
        'categoria_id',
        existing_type=sa.Integer(),
        nullable=True
    )
