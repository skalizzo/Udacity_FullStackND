"""added column completed

Revision ID: 28b4d3cd458c
Revises: 9fb763ec52c4
Create Date: 2020-03-27 13:27:14.094973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28b4d3cd458c'
down_revision = '9fb763ec52c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('completed', sa.Boolean(), nullable=True))
    
    op.execute('UPDATE todo SET completed = False WHERE completed IS NULL;')

    op.update_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todo', 'completed')
    # ### end Alembic commands ###
