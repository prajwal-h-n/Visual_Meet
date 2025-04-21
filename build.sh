#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Create database directory
mkdir -p /opt/render/project/

# Run database initialization script
echo "Running database initialization script"
python init_render_db.py

# Collect static files
python manage.py collectstatic --no-input

# Run migrations with more verbose output
python manage.py makemigrations
python manage.py migrate --no-input --verbosity 2

# Create a superuser if needed (optional)
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') if not User.objects.filter(username='admin').exists() else None" 