"""empty message

Revision ID: 7a2fe92bb1f7
Revises: 244d8d2a6c72
Create Date: 2022-08-01 08:18:30.159681

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7a2fe92bb1f7'
down_revision = '244d8d2a6c72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feed',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('owner_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('feed_games',
                    sa.Column('feed_id', sa.Integer(), nullable=False),
                    sa.Column('game_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
                    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
                    sa.PrimaryKeyConstraint('feed_id', 'game_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feed_games')
    op.drop_table('feed')
    # ### end Alembic commands ###
