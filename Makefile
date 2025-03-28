# Ensure POSIX compatibility
SHELL := /bin/sh

.PHONY: build clean init run test-data test

# Build the containers
build:
	docker compose build

# Clean up containers, volumes, and temporary files
clean:
	docker compose down -v --remove-orphans
	docker compose rm -f
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -f *.pyc */*.pyc */*/*.pyc
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf docs/_build

# Initialize the database with migrations
init:
	docker compose up -d db
	sleep 5  # Wait for database to be ready
	docker compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS flight_school;"
	docker compose exec db psql -U postgres -c "CREATE DATABASE flight_school;"
	docker compose exec db psql -U postgres -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
	docker compose run --rm web flask db init || true
	docker compose run --rm web flask db migrate -m "Initial migration"
	docker compose run --rm web flask db upgrade

# Run the application
run:
	docker compose up -d

# Load test data
test-data:
	docker compose run --rm web python load_test_data.py

# Run tests
test:
	docker compose run --rm web python -m pytest

# View logs
logs:
	docker compose logs -f

# Show container status
status:
	docker compose ps
