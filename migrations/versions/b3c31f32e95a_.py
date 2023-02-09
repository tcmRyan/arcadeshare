"""empty message

Revision ID: b3c31f32e95a
Revises: 1fb95f0bd628
Create Date: 2022-06-04 12:48:12.598115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c31f32e95a'
down_revision = '1fb95f0bd628'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('mac', sa.String(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('storage_slug', sa.String(), nullable=True),
    sa.Column('played', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('local_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('guid', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mqtt_acl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('allow', sa.Integer(), nullable=True),
    sa.Column('ipaddr', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('clientid', sa.String(), nullable=True),
    sa.Column('access', sa.Integer(), nullable=True),
    sa.Column('topic', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mqtt_acl_clientid'), 'mqtt_acl', ['clientid'], unique=False)
    op.create_index(op.f('ix_mqtt_acl_ipaddr'), 'mqtt_acl', ['ipaddr'], unique=False)
    op.create_index(op.f('ix_mqtt_acl_username'), 'mqtt_acl', ['username'], unique=False)
    op.add_column('user', sa.Column('salt', sa.String(), nullable=True))
    op.add_column('user', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'salt')
    op.drop_index(op.f('ix_mqtt_acl_username'), table_name='mqtt_acl')
    op.drop_index(op.f('ix_mqtt_acl_ipaddr'), table_name='mqtt_acl')
    op.drop_index(op.f('ix_mqtt_acl_clientid'), table_name='mqtt_acl')
    op.drop_table('mqtt_acl')
    op.drop_table('local_user')
    op.drop_table('game')
    op.drop_table('device')
    # ### end Alembic commands ###
