"""update enums

Revision ID: update_enums
Revises: add_timestamps
Create Date: 2024-03-29 06:24:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_enums'
down_revision = 'add_timestamps'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Drop the old enums if they exist
    op.execute("DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'flights_flight_type_check') THEN ALTER TABLE flights DROP CONSTRAINT flights_flight_type_check; END IF; END $$;")
    op.execute("DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'flights_status_check') THEN ALTER TABLE flights DROP CONSTRAINT flights_status_check; END IF; END $$;")
    
    # Temporarily change the columns to text type
    op.execute("ALTER TABLE flights ALTER COLUMN flight_type TYPE text")
    op.execute("ALTER TABLE flights ALTER COLUMN status TYPE text")
    
    # Drop the old enums
    op.execute("DROP TYPE IF EXISTS flighttype")
    op.execute("DROP TYPE IF EXISTS flightstatus")
    
    # Create new enums
    op.execute("CREATE TYPE flighttype AS ENUM ('training', 'solo', 'cross_country', 'night', 'instrument')")
    op.execute("CREATE TYPE flightstatus AS ENUM ('scheduled', 'completed', 'cancelled', 'in_progress')")
    
    # Convert existing data to match new enum values
    op.execute("UPDATE flights SET flight_type = LOWER(flight_type)")
    op.execute("UPDATE flights SET flight_type = 'training' WHERE flight_type = 'dual'")
    op.execute("UPDATE flights SET status = LOWER(status)")
    op.execute("UPDATE flights SET status = 'cancelled' WHERE status = 'no_show'")
    
    # Change the columns back to enum type
    op.execute("ALTER TABLE flights ALTER COLUMN flight_type TYPE flighttype USING flight_type::flighttype")
    op.execute("ALTER TABLE flights ALTER COLUMN status TYPE flightstatus USING status::flightstatus")

def downgrade() -> None:
    # Temporarily change the columns to text type
    op.execute("ALTER TABLE flights ALTER COLUMN flight_type TYPE text")
    op.execute("ALTER TABLE flights ALTER COLUMN status TYPE text")
    
    # Drop the new enums
    op.execute("DROP TYPE IF EXISTS flighttype")
    op.execute("DROP TYPE IF EXISTS flightstatus")
    
    # Create old enums
    op.execute("CREATE TYPE flighttype AS ENUM ('DUAL', 'SOLO', 'SIMULATOR', 'GROUND')")
    op.execute("CREATE TYPE flightstatus AS ENUM ('SCHEDULED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')")
    
    # Convert existing data to match old enum values
    op.execute("UPDATE flights SET flight_type = UPPER(flight_type)")
    op.execute("UPDATE flights SET flight_type = 'DUAL' WHERE flight_type = 'TRAINING'")
    op.execute("UPDATE flights SET status = UPPER(status)")
    op.execute("UPDATE flights SET status = 'NO_SHOW' WHERE status = 'CANCELLED'")
    
    # Change the columns back to enum type
    op.execute("ALTER TABLE flights ALTER COLUMN flight_type TYPE flighttype USING flight_type::flighttype")
    op.execute("ALTER TABLE flights ALTER COLUMN status TYPE flightstatus USING status::flightstatus") 