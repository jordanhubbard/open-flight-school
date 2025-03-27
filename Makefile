# Ensure POSIX compatibility
SHELL := /bin/sh

.PHONY: clean venv init test-data dev test setup reset-db lint format check coverage docs serve-docs migrate env help

# Clean up development files
clean:
	rm -rf venv
	rm -rf instance
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf docs/_build
	rm -f *.pyc */*.pyc */*/*.pyc

# Create and set up virtual environment
venv:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Initialize the database
init:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask db upgrade

# Load test data
test-data:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask seed-db

# Run the application
dev:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask run --port=5001

# Run tests
test:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	export FLASK_ENV=testing && \
	export TESTING=1 && \
	python -m pytest

# Run linting
lint:
	. venv/bin/activate && \
	flake8 . && \
	black . --check

# Format code
format:
	. venv/bin/activate && \
	black .

# Run all checks (lint, format, test)
check: lint format test

# Generate coverage report
coverage:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	export FLASK_ENV=testing && \
	export TESTING=1 && \
	python -m pytest --cov=app --cov-report=html

# Build documentation
docs:
	. venv/bin/activate && \
	cd docs && make html

# Serve documentation locally
serve-docs:
	. venv/bin/activate && \
	python -m http.server 8000 -d docs/_build/html

# Full development setup
setup: clean venv init test-data

# Reset database and reload test data
reset-db:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	rm -f instance/*.db && \
	flask db upgrade && \
	flask seed-db

# Create new migration
migrate:
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask db migrate -m "$(message)"

# Create new .env file from template
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from template. Please update the values."; \
	else \
		echo ".env file already exists."; \
	fi

# Show help
help:
	@echo "Available targets:"
	@echo "  setup      - Full development setup (clean, venv, init, test-data)"
	@echo "  dev        - Run the application"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting checks"
	@echo "  format     - Format code"
	@echo "  check      - Run all checks (lint, format, test)"
	@echo "  coverage   - Generate coverage report"
	@echo "  docs       - Build documentation"
	@echo "  serve-docs - Serve documentation locally"
	@echo "  reset-db   - Reset database and reload test data"
	@echo "  migrate    - Create new migration (use: make migrate message='migration message')"
	@echo "  env        - Create .env file from template"
	@echo "  clean      - Clean up development files"
