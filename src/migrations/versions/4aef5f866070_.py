"""empty message

Revision ID: 4aef5f866070
Revises: 05dac3e3e19b
Create Date: 2024-08-07 12:32:07.051283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aef5f866070'
down_revision = '05dac3e3e19b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fs_uniquifier', sa.UUID(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('fs_uniquifier')

    # ### end Alembic commands ###
