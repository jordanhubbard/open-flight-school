# Ensure POSIX compatibility
SHELL := /bin/sh

# Python version check
PYTHON := $(shell command -v python3 2> /dev/null)

# Check if virtual environment exists
VENV_EXISTS := $(shell [ -d venv ] && echo 1 || echo 0)

# Check if .env file exists
ENV_EXISTS := $(shell [ -f .env ] && echo 1 || echo 0)

.PHONY: clean venv init test-data dev test setup reset-db lint format check coverage docs serve-docs migrate env help check-env check-venv

# Check for virtual environment
check-venv:
	@if [ "$(VENV_EXISTS)" = "0" ]; then \
		echo "Virtual environment not found. Creating one..."; \
		$(MAKE) venv; \
	fi

# Check for .env file
check-env:
	@if [ "$(ENV_EXISTS)" = "0" ]; then \
		echo ".env file not found. Creating from template..."; \
		$(MAKE) env; \
	fi

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
	@echo "Cleaned up development files"

# Create and set up virtual environment
venv:
	@if [ -z "$(PYTHON)" ]; then \
		echo "Python 3 is not installed. Please install Python 3."; \
		exit 1; \
	fi
	@echo "Creating virtual environment..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Virtual environment created and dependencies installed"

# Initialize the database
init: check-venv check-env
	@echo "Initializing database..."
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	python -c "from database import init_db; init_db()"
	@echo "Database initialized"

# Load test data
test-data: check-venv check-env
	@echo "Loading test data..."
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	python -c "from database import init_db; from load_test_data import load_test_data; init_db(); load_test_data()"
	@echo "Test data loaded"

# Run the application
dev: check-venv check-env
	@echo "Starting development server..."
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask run --host=0.0.0.0 --port=5001

# Run tests
test: check-venv
	@echo "Running tests..."
	. venv/bin/activate && \
	export FLASK_ENV=testing && \
	export TESTING=1 && \
	python -m pytest
	@echo "Tests completed"

# Run linting
lint: check-venv
	@echo "Running linting checks..."
	. venv/bin/activate && \
	flake8 . && \
	black . --check
	@echo "Linting completed"

# Format code
format: check-venv
	@echo "Formatting code..."
	. venv/bin/activate && \
	black .
	@echo "Formatting completed"

# Run all checks (lint, format, test)
check: lint format test

# Generate coverage report
coverage: check-venv
	@echo "Generating coverage report..."
	. venv/bin/activate && \
	export FLASK_ENV=testing && \
	export TESTING=1 && \
	python -m pytest --cov=app --cov-report=html
	@echo "Coverage report generated in htmlcov/"

# Build documentation
docs: check-venv
	@echo "Building documentation..."
	. venv/bin/activate && \
	cd docs && make html
	@echo "Documentation built in docs/_build/html/"

# Serve documentation locally
serve-docs: docs
	@echo "Serving documentation on http://localhost:8000..."
	. venv/bin/activate && \
	python -m http.server 8000 -d docs/_build/html

# Full development setup
setup: clean env venv init test-data
	@echo "Development setup completed"

# Reset database and reload test data
reset-db: check-venv check-env
	@echo "Resetting database..."
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	rm -f instance/*.db && \
	python -c "from database import init_db; from load_test_data import load_test_data; init_db(); load_test_data()"
	@echo "Database reset and test data loaded"

# Create new migration
migrate: check-venv check-env
	@if [ -z "$(message)" ]; then \
		echo "Error: Migration message is required. Use: make migrate message='your message'"; \
		exit 1; \
	fi
	@echo "Creating new migration..."
	. venv/bin/activate && \
	export $$(cat .env | grep -v '^#' | xargs) && \
	flask db migrate -m "$(message)"
	@echo "Migration created"

# Create new .env file from template
env:
	@if [ ! -f .env ]; then \
		if [ ! -f .env.example ]; then \
			echo "Error: .env.example file not found"; \
			exit 1; \
		fi; \
		cp .env.example .env; \
		echo "Created .env file from template. Please update the values."; \
	else \
		echo ".env file already exists."; \
	fi

# Show help
help:
	@echo "Available targets:"
	@echo "  setup      - Full development setup (clean, env, venv, init, test-data)"
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
	@echo ""
	@echo "Note: Most targets will automatically check for and create virtual environment and .env file if needed."
