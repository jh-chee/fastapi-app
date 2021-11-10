"""add user table

Revision ID: 99ad75f8d450
Revises: 758d65cb0a4b
Create Date: 2021-11-10 21:22:55.821425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99ad75f8d450'
down_revision = '758d65cb0a4b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at',
                              sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), 
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
