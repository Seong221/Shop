"""empty message

Revision ID: bdf3f3068993
Revises: 
Create Date: 2024-05-20 18:05:53.167263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdf3f3068993'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Pistol Armory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pistol_type', sa.String(), nullable=False),
    sa.Column('pistol_name', sa.Text(), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Pistol Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_name'], ['Pistol Armory.pistol_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Pistol Users')
    op.drop_table('Pistol Armory')
    # ### end Alembic commands ###
