#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE flight_school_test;
    GRANT ALL PRIVILEGES ON DATABASE flight_school_test TO postgres;
EOSQL