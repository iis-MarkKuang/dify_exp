"""add-keyworg-table-storage-type

Revision ID: 17b5ab037c40
Revises: a8f9b3c45e4a
Create Date: 2024-04-01 09:48:54.232201

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "17b5ab037c40"
down_revision = "a8f9b3c45e4a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("dataset_keyword_tables", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "data_source_type",
                sa.String(length=255),
                server_default=sa.text("'database'::character varying"),
                nullable=False,
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("dataset_keyword_tables", schema=None) as batch_op:
        batch_op.drop_column("data_source_type")

    # ### end Alembic commands ###
