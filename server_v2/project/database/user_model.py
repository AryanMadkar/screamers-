from database.db import users_collection
from datetime import datetime
from uuid import uuid4

def create_user():
    user_id = str(uuid4())
    user ={
        "user_id": user_id,
         # In production, hash the password!
        "created_at": datetime.utcnow(),
        "last_seen": datetime.utcnow(),
        "active_conversations": None
    }
    
    users_collection.insert_one(user)
    return user_id

def user_exists(user_id):
    return users_collection.find_one({"user_id": user_id})


def update_last_seen(user_id):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"last_seen": datetime.utcnow()}}
    )
