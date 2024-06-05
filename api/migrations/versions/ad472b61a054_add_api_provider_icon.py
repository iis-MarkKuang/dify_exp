"""add api provider icon

Revision ID: ad472b61a054
Revises: 3ef9b2b6bee6
Create Date: 2024-01-07 02:21:23.114790

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ad472b61a054"
down_revision = "3ef9b2b6bee6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tool_api_providers", schema=None) as batch_op:
        batch_op.add_column(sa.Column("icon", sa.String(length=256), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tool_api_providers", schema=None) as batch_op:
        batch_op.drop_column("icon")

    # ### end Alembic commands ###
