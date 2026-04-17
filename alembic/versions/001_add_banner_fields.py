"""add banner_link and banner_label to articles and projects

Revision ID: 001_add_banner_fields
Revises:
Create Date: 2026-04-17
"""
from alembic import op
import sqlalchemy as sa

revision = "001_add_banner_fields"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("articles", sa.Column("banner_link", sa.String(), nullable=True))
    op.add_column("articles", sa.Column("banner_label", sa.String(), nullable=True))
    op.add_column("projects", sa.Column("banner_link", sa.String(), nullable=True))
    op.add_column("projects", sa.Column("banner_label", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("articles", "banner_label")
    op.drop_column("articles", "banner_link")
    op.drop_column("projects", "banner_label")
    op.drop_column("projects", "banner_link")
