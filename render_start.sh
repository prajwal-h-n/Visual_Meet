#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Running database migrations"
python manage.py makemigrations
python manage.py migrate

# Option: Create a superuser if needed (uncomment if desired)
# echo "Creating superuser"
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') if not User.objects.filter(username='admin').exists() else None"

echo "Starting server"
# Run the command passed to this script
exec "$@" 