#!/bin/bash

# Create test database
PGPASSWORD=postgres psql -h postgres -U postgres -c "DROP DATABASE IF EXISTS test_db;"
PGPASSWORD=postgres psql -h postgres -U postgres -c "CREATE DATABASE test_db;"

# Run migrations
alembic upgrade head

# Load test data
python load_test_data.py 