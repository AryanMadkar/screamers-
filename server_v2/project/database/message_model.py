from database.db import message_collection
from datetime import datetime
from uuid import uuid4


def save_message(conversation_id, sender, content):
    """
    FIX: Removed extra user_id param from original chat_service call signature.
    Canonical signature: (conversation_id, sender, content)
    """
    message_id = str(uuid4())
    message = {
        "message_id": message_id,
        "conversation_id": conversation_id,
        "sender": sender,
        "content": content,
        "timestamp": datetime.utcnow()
    }
    message_collection.insert_one(message)
    return message_id


def get_recent_messages(conversation_id, limit=20):
    # FIX: list().reverse() returns None (it's in-place).
    # Use sorted() or reverse the list after assignment.
    messages = list(
        message_collection.find(
            {"conversation_id": conversation_id}
        ).sort("timestamp", -1).limit(limit)
    )
    messages.reverse()  # reverse in-place on the list, not chained
    return messages
