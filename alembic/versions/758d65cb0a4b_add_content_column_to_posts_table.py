"""add content column to posts table

Revision ID: 758d65cb0a4b
Revises: bbbdc4bb9a11
Create Date: 2021-11-10 21:16:50.139680

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import nullslast


# revision identifiers, used by Alembic.
revision = '758d65cb0a4b'
down_revision = 'bbbdc4bb9a11'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content',
                            sa.String(),
                            nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
