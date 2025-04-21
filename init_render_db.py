"""
One-time script to initialize database on Render.com with MongoDB
"""
import os
import django
import subprocess

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoconferencing.settings')
django.setup()

# Print database configuration
from django.conf import settings
print(f"Database ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"Database NAME: {settings.DATABASES['default']['NAME']}")
if 'CLIENT' in settings.DATABASES['default'] and 'host' in settings.DATABASES['default']['CLIENT']:
    host = settings.DATABASES['default']['CLIENT']['host']
    # Hide credentials in the MongoDB URI for security
    if 'mongodb+srv://' in host:
        masked_uri = host.replace('://', '://****:****@')
        print(f"MongoDB URI: {masked_uri}")
    else:
        print(f"MongoDB URI: {host}")

# Run migrations
try:
    print("\nRunning migrations...")
    subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
    subprocess.run(['python', 'manage.py', 'migrate'], check=True)
except Exception as e:
    print(f"Error during migrations: {e}")

# Create superuser
try:
    print("\nChecking for admin user...")
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123!')
        print("Created superuser 'admin'")
    else:
        print("Admin user already exists")
except Exception as e:
    print(f"Error creating superuser: {e}")

print("\nDatabase initialization complete") 