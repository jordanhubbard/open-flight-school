"""add timestamps

Revision ID: add_timestamps
Revises: d3d9696d8106
Create Date: 2024-03-29 06:23:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_timestamps'
down_revision = 'd3d9696d8106'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add created_at and updated_at columns to all tables
    for table in ['users', 'aircraft', 'instructors', 'flights']:
        op.add_column(table, sa.Column('created_at', sa.DateTime(), nullable=True))
        op.add_column(table, sa.Column('updated_at', sa.DateTime(), nullable=True))
        
        # Set default values for existing rows
        op.execute(f"UPDATE {table} SET created_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP")
        
        # Make columns non-nullable
        op.alter_column(table, 'created_at', nullable=False)
        op.alter_column(table, 'updated_at', nullable=False)

def downgrade() -> None:
    # Remove created_at and updated_at columns from all tables
    for table in ['users', 'aircraft', 'instructors', 'flights']:
        op.drop_column(table, 'created_at')
        op.drop_column(table, 'updated_at') 