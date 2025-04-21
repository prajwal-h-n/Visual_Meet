#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting application setup..."

# Get PORT from environment
export PORT=${PORT:-10000}

# Force migrations for auth models first
echo "Forcing auth migrations..."
python manage.py migrate auth --noinput

# Then run all other migrations
echo "Running all migrations..."
python manage.py migrate --noinput

# Start server with the correct port binding
echo "Starting server on port $PORT"
exec python manage.py runserver 0.0.0.0:$PORT 