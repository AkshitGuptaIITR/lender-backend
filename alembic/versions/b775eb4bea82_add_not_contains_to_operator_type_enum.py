"""Add NOT_CONTAINS to operator_type enum

Revision ID: b775eb4bea82
Revises: a672c977ceae
Create Date: 2026-01-05 02:56:25.069575

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b775eb4bea82"
down_revision: Union[str, Sequence[str], None] = "a672c977ceae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE operator_type ADD VALUE 'NOT_CONTAINS'")


def downgrade() -> None:
    """Downgrade schema."""
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE operator_type DROP VALUE 'NOT_CONTAINS'")
