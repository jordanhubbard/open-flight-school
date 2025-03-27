.PHONY: build up down logs test clean db-reset init test-data

# Build the containers
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

# Clean up containers, volumes, and images
clean:
	docker compose down -v
	docker compose rm -f
	docker system prune -f

# Reset the database (drop and recreate)
db-reset:
	docker compose down -v
	docker compose up -d db
	sleep 5  # Wait for database to be ready
	docker compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS flight_school;"
	docker compose exec db psql -U postgres -c "CREATE DATABASE flight_school;"
	docker compose exec db psql -U postgres -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

# Initialize the database with migrations
init: db-reset
	docker compose run --rm migrations

# Load test data
test-data:
	docker compose run --rm load-test-data

# Development workflow: build, init, and start
dev: build init test-data up

# Production workflow: build and start
prod: build up

# Show container status
status:
	docker compose ps

# Rebuild and restart a specific service
restart:
	docker compose restart $(service)

# View logs for a specific service
service-logs:
	docker compose logs -f $(service)
