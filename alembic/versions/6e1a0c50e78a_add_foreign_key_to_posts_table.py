"""add foreign key to posts table

Revision ID: 6e1a0c50e78a
Revises: 99ad75f8d450
Create Date: 2021-11-10 21:30:21.271809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e1a0c50e78a'
down_revision = '99ad75f8d450'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table="posts",
                          referent_table="users",
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE"
                          )


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_constraint("posts", "owner_id")
