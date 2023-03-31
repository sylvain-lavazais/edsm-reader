#!/bin/sh -e

if [ $1 != "python" ]; then
    exec "$@"
fi

# Waiting for Database to be operational
echo "Waiting for database to be operational... (20 sec)"
sleep 20

exec "$@"
