"""Init role

Revision ID: 22395ac4b7b3
Revises: 8df0a909c835
Create Date: 2024-07-29 21:37:03.942831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22395ac4b7b3'
down_revision: Union[str, None] = '8df0a909c835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE role as ENUM('admin', 'moderator', 'user')")
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='role'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    op.execute("DROP TYPE role")
    # ### end Alembic commands ###
