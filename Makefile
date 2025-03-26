.PHONY: setup init run test clean db-reset clean-db

setup:
	python3.11 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

init: db-reset
	. venv/bin/activate && flask db upgrade

run:
	. venv/bin/activate && flask run

test:
	. venv/bin/activate && python -m pytest
	. venv/bin/activate && python load_test_data.py

test-data: setup
	python3.11 -m venv venv

clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf instance
	rm -rf migrations

db-reset:
	psql -U postgres -h localhost -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'flight_school' AND pid <> pg_backend_pid();"
	psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS flight_school;"
	psql -U postgres -h localhost -c "CREATE DATABASE flight_school;"
	psql -U postgres -h localhost -d flight_school -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" 

clean-db: db-reset
	rm -rf migrations
	${MAKE} setup
	. venv/bin/activate && flask db init
	. venv/bin/activate && flask db migrate -m "Initial migration"
	. venv/bin/activate && flask db upgrade
