#!/bin/bash
set -e

if [ "$FLASK_DEBUG" = "1" ]; then
  echo "Starting Flask development server with hot reloading..."
  exec flask run --host=0.0.0.0 --port=5000 --reload
else
  echo "Starting Gunicorn production server..."
  exec gunicorn --bind 0.0.0.0:5000 app:app
fi
