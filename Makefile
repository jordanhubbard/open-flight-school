.PHONY: build up down logs test clean db-reset init test-data local-clean local-dev local-init local-test-data

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

# Clean up containers and volumes
clean:
	docker compose down -v --remove-orphans
	docker compose rm -f
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf instance
	rm -rf migrations
	rm -f *.pyc */*.pyc */*/*.pyc
	rm -f *.sqlite *.sqlite3 *.db

# Deep clean - includes docker system prune
deep-clean: clean
	docker system prune -f

# Reset the database (drop and recreate)
db-reset:
	docker compose down -v --remove-orphans
	docker compose up -d db
	sleep 5  # Wait for database to be ready
	docker compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS flight_school;"
	docker compose exec db psql -U postgres -c "CREATE DATABASE flight_school;"
	docker compose exec db psql -U postgres -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

# Initialize migrations
init-migrations:
	docker compose run --rm web flask db init
	docker compose run --rm web flask db migrate -m "Initial migration"
	docker compose run --rm web flask db upgrade

# Initialize the database with migrations
init: db-reset init-migrations

# Load test data
test-data:
	docker compose run --rm web python load_test_data.py

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
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf instance
	rm -rf migrations
	rm -f *.pyc */*.pyc */*/*.pyc
	rm -f *.sqlite *.sqlite3 *.db

# Initialize local virtual environment
local-venv:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Initialize local database and migrations
local-init:
	@if [ ! -f .env ]; then \
		echo "Creating default .env file..."; \
		echo "SECRET_KEY=local-dev-key" > .env; \
		echo "FLASK_APP=app.py" >> .env; \
		echo "FLASK_ENV=development" >> .env; \
		echo "DATABASE_URL=sqlite:///flight_school.db" >> .env; \
		echo "MAIL_SERVER=localhost" >> .env; \
		echo "MAIL_PORT=1025" >> .env; \
		echo "MAIL_USE_TLS=False" >> .env; \
		echo "MAIL_USERNAME=test" >> .env; \
		echo "MAIL_PASSWORD=test" >> .env; \
		echo "BASE_URL=http://localhost:5001" >> .env; \
	fi
	. venv/bin/activate && \
	set -a && source .env && set +a && \
	flask db init && \
	flask db migrate -m "Initial migration" && \
	flask db upgrade

# Load test data locally
local-test-data:
	. venv/bin/activate && set -a && source .env && set +a && python load_test_data.py

# Setup and run local development environment
local-dev: local-clean local-venv local-init local-test-data
	@echo "\nStarting Flask development server..."
	. venv/bin/activate && set -a && source .env && set +a && flask run --port 5001

# Run tests locally
local-test:
	. venv/bin/activate && python -m pytest
