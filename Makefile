# Ensure POSIX compatibility
SHELL := /bin/sh

.PHONY: build clean init run test-data test backend-test frontend-test

# Build the containers
build:
	docker compose build

# Clean up containers, volumes, and temporary files
clean:
	docker compose down -v --remove-orphans
	docker compose rm -f
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name "node_modules" -exec rm -r {} +
	find . -type f -name "*.log" -delete

# Initialize the database with migrations
init:
	docker compose up -d db
	sleep 5  # Wait for database to be ready
	docker compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS flight_school;"
	docker compose exec db psql -U postgres -c "CREATE DATABASE flight_school;"
	docker compose exec db psql -U postgres -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
	docker compose run --rm backend alembic init alembic || true
	docker compose run --rm backend alembic revision --autogenerate -m "Initial migration"
	docker compose run --rm backend alembic upgrade head

# Run the application
run:
	docker compose up -d

# Load test data
test-data:
	docker compose run --rm backend python load_test_data.py

# Run backend tests
backend-test:
	docker compose run --rm backend python -m pytest

# Run frontend tests
frontend-test:
	cd frontend && npm test

# Run all tests (both frontend and backend)
test: backend-test frontend-test

# View logs
logs:
	docker compose logs -f

# Show container status
status:
	docker compose ps
