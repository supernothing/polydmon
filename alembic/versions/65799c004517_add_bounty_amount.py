"""add bounty amount

Revision ID: 65799c004517
Revises: 809932e97d97
Create Date: 2020-04-28 17:56:54.160311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65799c004517'
down_revision = '809932e97d97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bounty', sa.Column('amount', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bounty', 'amount')
    # ### end Alembic commands ###
