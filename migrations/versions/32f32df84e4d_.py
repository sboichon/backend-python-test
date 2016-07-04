"""Add is_completed column to todo

Revision ID: 32f32df84e4d
Revises: cf4cd08bd49e
Create Date: 2016-07-04 15:49:13.876848

"""

# revision identifiers, used by Alembic.
revision = '32f32df84e4d'
down_revision = 'cf4cd08bd49e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('todos', sa.Column('is_completed',
                                     sa.Boolean,
                                     nullable=False,
                                     server_default=sa.false()))


def downgrade():
    op.drop_column('todos', 'is_completed')
