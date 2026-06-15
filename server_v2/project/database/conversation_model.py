from database.db import conversations_collection
from datetime import datetime
from uuid import uuid4


def create_conversation(user_id):
    conversation_id = str(uuid4())
    conversation = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "started_at": datetime.utcnow(),
        "ended_at": None,
        "status": "active",
        "summary": "",
        "total_messages": 0
    }
    conversations_collection.insert_one(conversation)
    return conversation_id


def get_active_conversations(user_id):
    conversations = conversations_collection.find({"user_id": user_id, "status": "active"})
    return list(conversations)


# FIX: Renamed from increment_message_count → increment_conversation_count
# to match the name used in chat_service.py
def increment_conversation_count(conversation_id):
    conversations_collection.update_one(
        {"conversation_id": conversation_id},
        {"$inc": {"total_messages": 1}}
    )


def end_conversation(conversation_id):
    conversations_collection.update_one(
        {"conversation_id": conversation_id},
        {"$set": {"status": "ended", "ended_at": datetime.utcnow()}}
    )

