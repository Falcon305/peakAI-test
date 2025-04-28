#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 3

# Initialize the database
echo "Initializing database..."
python init_db.py

if [ "$FLASK_DEBUG" = "1" ]; then
  echo "Starting Flask development server with hot reloading..."
  exec flask run --host=0.0.0.0 --port=5000 --reload
else
  echo "Starting Gunicorn production server..."
  exec gunicorn --bind 0.0.0.0:5000 app:app
fi
