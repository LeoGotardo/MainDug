"""primeira fixed

Revision ID: bb5eaa7d6682
Revises: ee2001767e9d
Create Date: 2024-06-05 14:57:28.391669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb5eaa7d6682'
down_revision: Union[str, None] = 'ee2001767e9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
