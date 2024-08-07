"""empty message

Revision ID: ca3e3ceb1b31
Revises: ee7727a80e29
Create Date: 2022-08-10 08:01:30.723183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3e3ceb1b31'
down_revision = 'ee7727a80e29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.drop_column('user', 'emqx_pwd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('emqx_pwd', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    # ### end Alembic commands ###