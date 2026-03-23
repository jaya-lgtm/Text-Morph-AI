from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os

# MongoDB Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["infosys_db"]

def get_users_collection():
    """Returns the users collection"""
    return db["users"]

def get_history_collection():
    """Returns the history collection"""
    return db["history"]

def create_indexes():
    """Create necessary indexes for MongoDB collections"""
    users_col = get_users_collection()
    history_col = get_history_collection()
    
    # Create unique index on username
    try:
        users_col.create_index("username", unique=True)
    except Exception as e:
        print(f"Index creation warning: {e}")
    
    # Create index on username for history collection to speed up queries
    try:
        history_col.create_index("username")
    except Exception as e:
        print(f"Index creation warning: {e}")