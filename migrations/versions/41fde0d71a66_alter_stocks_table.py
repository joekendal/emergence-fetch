"""alter stocks table

Revision ID: 41fde0d71a66
Revises:
Create Date: 2019-07-24 06:25:18.805101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41fde0d71a66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'stocks',
        'id',
        new_column_name='symbol'
    )
    op.add_column(
        'stocks',
        sa.Column('name', sa.String())
    )


def downgrade():
    pass
