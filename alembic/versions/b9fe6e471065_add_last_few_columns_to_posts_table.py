"""add last few columns to posts table

Revision ID: b9fe6e471065
Revises: 6e1a0c50e78a
Create Date: 2021-11-10 21:35:03.142299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9fe6e471065'
down_revision = '6e1a0c50e78a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('published',
                            sa.Boolean(),
                            nullable=False,
                            server_default='TRUE')
                  )
    op.add_column('posts',
                  sa.Column('created_at',
                            sa.TIMESTAMP(timezone=True),
                            nullable=False,
                            server_default=sa.text('NOW()')
                            )
                  )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
