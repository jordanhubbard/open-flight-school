#!/bin/bash

# Set up the test database
./tests/setup_test_db.sh

# Run the tests from /app directory with correct PYTHONPATH
cd /app && PYTHONPATH=/app pytest tests/ -v 