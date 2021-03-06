"""add bounty guid

Revision ID: 65fa64085de5
Revises: 6c69060c93e8
Create Date: 2020-04-28 16:29:14.873158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65fa64085de5'
down_revision = '6c69060c93e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assertion', sa.Column('bounty_guid', sa.String(), nullable=True))
    op.create_index(op.f('ix_assertion_bounty_guid'), 'assertion', ['bounty_guid'], unique=False)
    op.add_column('vote', sa.Column('address', sa.String(), nullable=True))
    op.add_column('vote', sa.Column('bounty_guid', sa.String(), nullable=True))
    op.create_index(op.f('ix_vote_address'), 'vote', ['address'], unique=False)
    op.create_index(op.f('ix_vote_bounty_guid'), 'vote', ['bounty_guid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vote_bounty_guid'), table_name='vote')
    op.drop_index(op.f('ix_vote_address'), table_name='vote')
    op.drop_column('vote', 'bounty_guid')
    op.drop_column('vote', 'address')
    op.drop_index(op.f('ix_assertion_bounty_guid'), table_name='assertion')
    op.drop_column('assertion', 'bounty_guid')
    # ### end Alembic commands ###
