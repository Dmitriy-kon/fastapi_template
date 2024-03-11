"""delete salt

Revision ID: 6535cf68e19f
Revises: 813290154e3e
Create Date: 2024-03-11 11:19:34.766662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6535cf68e19f'
down_revision: Union[str, None] = '813290154e3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'salt')


def downgrade() -> None:
    pass
