.PHONY: setup run test clean init-db init db-reset test-data

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
FLASK = $(VENV)/bin/flask
PSQL = psql -U postgres -h localhost

setup: $(VENV)
	$(PIP) install -r requirements.txt
	$(FLASK) db init
	$(FLASK) db migrate -m "Initial migration"
	$(FLASK) db upgrade
	$(PYTHON) init_db.py

$(VENV):
	python3 -m venv $(VENV)

run: $(VENV)
	$(FLASK) run

test: $(VENV)
	$(PYTHON) -m pytest tests/

clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf instance
	rm -rf migrations

init-db: $(VENV)
	$(PYTHON) init_db.py

db-reset:
	@psql -U postgres -h localhost -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'flight_school' AND pid <> pg_backend_pid();"
	@psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS flight_school;"
	@psql -U postgres -h localhost -c "CREATE DATABASE flight_school;"
	@psql -U postgres -h localhost -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
	@psql -U postgres -h localhost -d flight_school -c "DROP TABLE IF EXISTS users, aircraft, instructor, booking CASCADE;"

init: clean db-reset $(VENV)
	$(PIP) install -r requirements.txt
	$(FLASK) db init
	$(FLASK) db migrate -m "Initial migration"
	$(FLASK) db upgrade
	$(PYTHON) init_db.py
	@echo "Database initialized with correct schema. Tables created: users, aircraft, instructor, booking"

test-data: $(VENV)
	@echo "Loading test data..."
	$(PYTHON) scripts/load_test_data.py 