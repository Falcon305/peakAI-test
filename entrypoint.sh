#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

MAX_RETRIES=30
RETRY_COUNT=0

until pg_isready -h db -U postgres || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
  echo "Waiting for database connection..."
  RETRY_COUNT=$((RETRY_COUNT+1))
  sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "Failed to connect to database after $MAX_RETRIES attempts!"
  exit 1
fi

sleep 3

echo "Initializing database..."
python init_db.py

echo "Verifying database schema..."
PGPASSWORD=postgres psql -h db -U postgres -d postgres -c "\dt" | grep -q users || {
  echo "Tables not properly created, retrying initialization..."
  python init_db.py
}

if [ "$FLASK_DEBUG" = "1" ]; then
  echo "Starting Flask development server with hot reloading..."
  exec flask run --host=0.0.0.0 --port=5000 --reload
else
  echo "Starting Gunicorn production server..."
  exec gunicorn --bind 0.0.0.0:5000 app:app
fi
