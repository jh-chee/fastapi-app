"""create posts table

Revision ID: bbbdc4bb9a11
Revises: 
Create Date: 2021-11-10 21:09:07.104120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbbdc4bb9a11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',
                              sa.INTEGER(),
                              nullable=False,
                              primary_key=True
                              ),
                    sa.Column('title',
                              sa.String(),
                              nullable=False
                              )
                    )


def downgrade():
    op.drop_table('posts')
    pass
