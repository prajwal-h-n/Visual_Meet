#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Create a specific start script for Render
cat > start.sh << 'EOL'
#!/usr/bin/env bash
# Get PORT from environment
export PORT=${PORT:-8000}
echo "Starting server on port $PORT"

# Run migrations
python manage.py migrate

# Start server with the correct port binding
python manage.py runserver 0.0.0.0:$PORT
EOL

# Make start script executable
chmod +x start.sh

# Collect static files
python manage.py collectstatic --no-input

# Create database directory
mkdir -p /opt/render/project/

# Run database initialization script
echo "Running database initialization script"
python init_render_db.py

# Run migrations with more verbose output
python manage.py makemigrations
python manage.py migrate --no-input --verbosity 2

# Create a superuser if needed (optional)
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') if not User.objects.filter(username='admin').exists() else None" 