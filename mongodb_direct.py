"""
Alternative MongoDB implementation using direct PyMongo.
If Djongo continues to have compatibility issues, replace the DATABASE section
in settings.py with the code from this file.
"""

from pymongo import MongoClient
import os

# Get MongoDB URI from environment variable or use default
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/videoconferencedb')

# Connect to MongoDB directly
mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client.get_database()

# Use Django's default database for auth and sessions
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom backends for MongoDB access
# You'll need to create functions that use mongo_db for data storage
# Example usage in a view:
#
# from django.conf import settings
# mongo_db = settings.mongo_db
# user_collection = mongo_db['users']
# user_data = {
#     'email': form.cleaned_data['email'],
#     'first_name': form.cleaned_data['first_name'],
#     'last_name': form.cleaned_data['last_name'],
#     'password': form.cleaned_data['password1'],  # Should be hashed
# }
# user_collection.insert_one(user_data) 