from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "<PUT_HASH_HERE>"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("author", sa.String(length=120), nullable=True),
    )

def downgrade() -> None:
    op.drop_table("notes")
