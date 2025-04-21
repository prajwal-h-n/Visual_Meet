#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Creating database directory if it doesn't exist"
mkdir -p /opt/render/project/

echo "Running initial migrations for auth models"
python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate sessions

echo "Running remaining migrations"
python manage.py makemigrations videoconference_app
python manage.py migrate

# Create a superuser for admin access (uncomment and change credentials as needed)
echo "Creating superuser"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123!') if not User.objects.filter(username='admin').exists() else print('Admin user already exists')"

echo "Starting server"
# Run the command passed to this script
exec "$@" 