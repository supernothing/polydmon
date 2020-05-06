"""create tables

Revision ID: 1491e41ee71b
Revises: 
Create Date: 2020-04-28 15:56:28.670957

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1491e41ee71b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bounty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.Column('txhash', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('guid', sa.String(), nullable=True),
    sa.Column('md5', sa.String(), nullable=True),
    sa.Column('sha1', sa.String(), nullable=True),
    sa.Column('sha256', sa.String(), nullable=True),
    sa.Column('mimetype', sa.String(), nullable=True),
    sa.Column('extended_type', sa.String(), nullable=True),
    sa.Column('uri', sa.String(), nullable=True),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bounty_block_number'), 'bounty', ['block_number'], unique=False)
    op.create_index(op.f('ix_bounty_event'), 'bounty', ['event'], unique=False)
    op.create_index(op.f('ix_bounty_guid'), 'bounty', ['guid'], unique=False)
    op.create_index(op.f('ix_bounty_md5'), 'bounty', ['md5'], unique=False)
    op.create_index(op.f('ix_bounty_sha1'), 'bounty', ['sha1'], unique=False)
    op.create_index(op.f('ix_bounty_sha256'), 'bounty', ['sha256'], unique=False)
    op.create_index(op.f('ix_bounty_txhash'), 'bounty', ['txhash'], unique=False)
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.Column('txhash', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_block_number'), 'event', ['block_number'], unique=False)
    op.create_index(op.f('ix_event_event'), 'event', ['event'], unique=False)
    op.create_index(op.f('ix_event_txhash'), 'event', ['txhash'], unique=False)
    op.create_table('assertion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.Column('txhash', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('bounty_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('bid', sa.BigInteger(), nullable=True),
    sa.Column('assertion', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['bounty_id'], ['bounty.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assertion_address'), 'assertion', ['address'], unique=False)
    op.create_index(op.f('ix_assertion_assertion'), 'assertion', ['assertion'], unique=False)
    op.create_index(op.f('ix_assertion_block_number'), 'assertion', ['block_number'], unique=False)
    op.create_index(op.f('ix_assertion_bounty_id'), 'assertion', ['bounty_id'], unique=False)
    op.create_index(op.f('ix_assertion_event'), 'assertion', ['event'], unique=False)
    op.create_index(op.f('ix_assertion_txhash'), 'assertion', ['txhash'], unique=False)
    op.create_table('vote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.Column('txhash', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('bounty_id', sa.Integer(), nullable=True),
    sa.Column('vote', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['bounty_id'], ['bounty.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vote_block_number'), 'vote', ['block_number'], unique=False)
    op.create_index(op.f('ix_vote_bounty_id'), 'vote', ['bounty_id'], unique=False)
    op.create_index(op.f('ix_vote_event'), 'vote', ['event'], unique=False)
    op.create_index(op.f('ix_vote_txhash'), 'vote', ['txhash'], unique=False)
    op.create_index(op.f('ix_vote_vote'), 'vote', ['vote'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vote_vote'), table_name='vote')
    op.drop_index(op.f('ix_vote_txhash'), table_name='vote')
    op.drop_index(op.f('ix_vote_event'), table_name='vote')
    op.drop_index(op.f('ix_vote_bounty_id'), table_name='vote')
    op.drop_index(op.f('ix_vote_block_number'), table_name='vote')
    op.drop_table('vote')
    op.drop_index(op.f('ix_assertion_txhash'), table_name='assertion')
    op.drop_index(op.f('ix_assertion_event'), table_name='assertion')
    op.drop_index(op.f('ix_assertion_bounty_id'), table_name='assertion')
    op.drop_index(op.f('ix_assertion_block_number'), table_name='assertion')
    op.drop_index(op.f('ix_assertion_assertion'), table_name='assertion')
    op.drop_index(op.f('ix_assertion_address'), table_name='assertion')
    op.drop_table('assertion')
    op.drop_index(op.f('ix_event_txhash'), table_name='event')
    op.drop_index(op.f('ix_event_event'), table_name='event')
    op.drop_index(op.f('ix_event_block_number'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_bounty_txhash'), table_name='bounty')
    op.drop_index(op.f('ix_bounty_sha256'), table_name='bounty')
    op.drop_index(op.f('ix_bounty_sha1'), table_name='bounty')
    op.drop_index(op.f('ix_bounty_md5'), table_name='bounty')
    op.drop_index(op.f('ix_bounty_guid'), table_name='bounty')
    op.drop_index(op.f('ix_bounty_event'), table_name='bounty')
    op.drop_index(op.f('ix_bounty_block_number'), table_name='bounty')
    op.drop_table('bounty')
    # ### end Alembic commands ###
