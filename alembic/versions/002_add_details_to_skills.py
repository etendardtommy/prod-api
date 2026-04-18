"""add details to skills

Revision ID: 002_add_details_to_skills
Revises: 001_add_banner_fields
Create Date: 2026-04-18
"""
from alembic import op
import sqlalchemy as sa

revision = "002_add_details_to_skills"
down_revision = "001_add_banner_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("skills", sa.Column("details", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("skills", "details")
