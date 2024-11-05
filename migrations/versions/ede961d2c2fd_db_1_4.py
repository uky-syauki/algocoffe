"""db 1.4

Revision ID: ede961d2c2fd
Revises: 568ce73288a6
Create Date: 2024-11-05 22:26:14.566644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ede961d2c2fd'
down_revision = '568ce73288a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alamat', sa.String(length=64), nullable=True))

    with op.batch_alter_table('coffe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coffe', schema=None) as batch_op:
        batch_op.drop_column('rating')

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('alamat')

    # ### end Alembic commands ###
