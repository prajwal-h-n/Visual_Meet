"""
Quick script to check users in the database.
Run with: python check_users.py
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoconferencing.settings')
django.setup()

# Import User model
from django.contrib.auth.models import User

def list_all_users():
    """List all users in the database"""
    print("\n==== ALL USERS ====")
    users = User.objects.all()
    if not users:
        print("No users found in the database!")
    else:
        print(f"Found {users.count()} users:")
        for user in users:
            print(f"- ID: {user.id}, Username: {user.username}, Email: {user.email}")

def check_specific_user(username):
    """Check if a specific user exists"""
    print(f"\n==== CHECKING USER: {username} ====")
    try:
        user = User.objects.get(username=username)
        print(f"User found: ID={user.id}, Username={user.username}, Email={user.email}")
        return True
    except User.DoesNotExist:
        print(f"User '{username}' does not exist!")
        return False
    except Exception as e:
        print(f"Error checking user: {e}")
        return False

def create_test_user():
    """Create a test user for debugging"""
    print("\n==== CREATING TEST USER ====")
    try:
        username = "testuser@example.com"
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists!")
            return
            
        user = User.objects.create_user(
            username=username,
            email=username,
            password="Test1234!",
            first_name="Test",
            last_name="User"
        )
        print(f"Test user created: ID={user.id}, Username={user.username}")
    except Exception as e:
        print(f"Error creating test user: {e}")

if __name__ == "__main__":
    print("=== USER DATABASE CHECK ===")
    
    # List all users
    list_all_users()
    
    # Check specific user
    check_specific_user("user122@gmail.com")
    
    # Create test user if needed
    create_test_user()
    
    # List users again
    list_all_users() 