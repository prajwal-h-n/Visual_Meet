"""
One-time script to initialize database on Render.com
"""
import os
import django
import subprocess
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoconferencing.settings')
django.setup()

# Ensure persistent directory exists
PERSISTENT_DIR = '/opt/render/project'
if not os.path.exists(PERSISTENT_DIR):
    os.makedirs(PERSISTENT_DIR)
    print(f"Created directory: {PERSISTENT_DIR}")

# Print database configuration
from django.conf import settings
print(f"Database location: {settings.DATABASES['default']['NAME']}")

# Check if auth_user table exists
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
        result = cursor.fetchone()
        if result:
            print("auth_user table exists")
        else:
            print("auth_user table DOES NOT exist")
except Exception as e:
    print(f"Error checking table: {e}")

# Run migrations
try:
    print("Running migrations for auth models...")
    subprocess.run(['python', 'manage.py', 'migrate', 'auth'], check=True)
    subprocess.run(['python', 'manage.py', 'migrate', 'admin'], check=True)
    subprocess.run(['python', 'manage.py', 'migrate', 'sessions'], check=True)
    subprocess.run(['python', 'manage.py', 'migrate', 'contenttypes'], check=True)
    
    print("Running remaining migrations...")
    subprocess.run(['python', 'manage.py', 'makemigrations', 'videoconference_app'], check=True)
    subprocess.run(['python', 'manage.py', 'migrate'], check=True)
except Exception as e:
    print(f"Error during migrations: {e}")

# Create superuser
try:
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123!')
        print("Created superuser 'admin'")
    else:
        print("Admin user already exists")
except Exception as e:
    print(f"Error creating superuser: {e}")

print("Database initialization complete") 