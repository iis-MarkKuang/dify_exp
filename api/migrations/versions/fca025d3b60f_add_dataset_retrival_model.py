"""add-dataset-retrival-model

Revision ID: fca025d3b60f
Revises: b3a09c049e8e
Create Date: 2023-11-03 13:08:23.246396

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fca025d3b60f"
down_revision = "8fe468ba0ca5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("sessions")
    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.add_column(sa.Column("retrieval_model", postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        batch_op.create_index("retrieval_model_idx", ["retrieval_model"], unique=False, postgresql_using="gin")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.drop_index("retrieval_model_idx", postgresql_using="gin")
        batch_op.drop_column("retrieval_model")

    op.create_table(
        "sessions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column("data", postgresql.BYTEA(), autoincrement=False, nullable=True),
        sa.Column("expiry", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="sessions_pkey"),
        sa.UniqueConstraint("session_id", name="sessions_session_id_key"),
    )
    # ### end Alembic commands ###
