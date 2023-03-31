#!/bin/sh
set -e

PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    \connect "astraeus-db"
    CREATE SCHEMA "astraeus";
    ALTER SCHEMA "astraeus" OWNER TO "astraeus";
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
