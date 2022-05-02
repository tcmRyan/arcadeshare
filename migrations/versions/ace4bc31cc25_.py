"""empty message

Revision ID: ace4bc31cc25
Revises: 465bc8d44a39
Create Date: 2022-04-25 08:51:27.608982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ace4bc31cc25'
down_revision = '465bc8d44a39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tenant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('user', sa.Column('tenant_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'tenant', ['tenant_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'tenant_id')
    op.drop_table('tenant')
    # ### end Alembic commands ###
