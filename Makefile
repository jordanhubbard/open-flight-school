# Ensure POSIX compatibility
SHELL := /bin/sh

.PHONY: build up down logs test clean db-reset init test-data local-clean local-dev local-init local-test-data

# Docker commands
build:
	docker compose build

# Start the application
up:
	docker compose up -d

# Stop the application
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# Run tests
test:
	docker compose run --rm web python -m pytest

# Clean up containers and volumes
clean:
	docker compose down -v
	rm -rf instance/*.db

# Reset the database (drop and recreate)
db-reset:
	docker compose down -v
	rm -rf instance/*.db
	docker compose up -d
	flask db upgrade
	flask seed-db

# Initialize the database with migrations
init:
	docker compose up -d
	flask db upgrade

# Load test data
test-data:
	flask seed-db

# Development workflow: build, init, and start (without test data)
dev: build init up

# Development workflow with test data
dev-with-test-data: build init test-data up

# Production workflow: build and start
prod: build
	docker compose up -d db
	sleep 5  # Wait for database to be ready
	docker compose exec db psql -U postgres -c "CREATE DATABASE flight_school;" || true
	docker compose exec db psql -U postgres -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" || true
	docker compose run --rm web flask db init || true
	docker compose run --rm web flask db migrate -m "Initial migration"
	docker compose run --rm web flask db upgrade
	docker compose up -d

# Production workflow with test data
prod-with-test-data: prod test-data

# Show container status
status:
	docker compose ps

# Rebuild and restart a specific service
restart:
	docker compose restart $(service)

# View logs for a specific service
service-logs:
	docker compose logs -f $(service)

# Clean local development files
local-clean:
	rm -rf venv
	rm -rf instance
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

# Initialize local virtual environment
local-venv:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Initialize local database
local-init:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask db upgrade

# Load test data locally
local-test-data:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask seed-db

# Setup and run local development environment
local-dev:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask run --port=5001

# Run tests locally
local-test:
	{ \
		. ./venv/bin/activate; \
		python -m pytest; \
	}
