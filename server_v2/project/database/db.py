from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI, maxPoolSize=50, minPoolSize=10)

db = client[Config.DB_NAME]

users_collection = db['users']
conversations_collection = db['conversations']
message_collection = db['messages']


def create_indexes():
    users_collection.create_index("user_id", unique=True)

    conversations_collection.create_index("conversation_id", unique=True)
    conversations_collection.create_index("user_id")

    message_collection.create_index(
        [("conversation_id", 1), ("timestamp", 1)]
    )
    message_collection.create_index("user_id")
