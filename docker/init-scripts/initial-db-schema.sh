#!/bin/sh
set -e

PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    \connect "edsm-mirror"
    CREATE SCHEMA "edsm-mirror";
    ALTER SCHEMA "edsm-mirror" OWNER TO "edsm-mirror";
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
