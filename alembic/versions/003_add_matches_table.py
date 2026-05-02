"""add matches table

Revision ID: 003_add_matches_table
Revises: 002_add_details_to_skills
Create Date: 2026-05-02
"""
from alembic import op
import sqlalchemy as sa

revision = "003_add_matches_table"
down_revision = "002_add_details_to_skills"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("site_id", sa.Integer(), nullable=False, index=True),
        sa.Column("eva_match_id", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("tournament_id", sa.String(), nullable=False),
        sa.Column("tournament_name", sa.String(), nullable=False),
        sa.Column("division", sa.String(), nullable=True),
        sa.Column("opponent_name", sa.String(), nullable=False),
        sa.Column("opponent_logo_url", sa.String(), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("played_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("score_eclyps", sa.Integer(), nullable=True),
        sa.Column("score_opponent", sa.Integer(), nullable=True),
        sa.Column("result", sa.String(), nullable=True),
        sa.Column("synced_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("matches")
