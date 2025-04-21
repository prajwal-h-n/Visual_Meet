#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Running migrations"
python manage.py makemigrations
python manage.py migrate

# Create a superuser for admin access
echo "Creating superuser"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123!') if not User.objects.filter(username='admin').exists() else print('Admin user already exists')"

echo "Starting server"
# Get the PORT environment variable
export PORT=${PORT:-8000}
echo "Using port: $PORT"

# Start the server with the correct port
exec gunicorn videoconferencing.wsgi:application --bind 0.0.0.0:$PORT 