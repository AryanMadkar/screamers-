from database.message_model import (
    save_message,
    get_recent_messages,
)
from database.conversation_model import (
    increment_conversation_count,
)

class MessageManager:
    @staticmethod
    def save_user_message(conversation_id, message):
        save_message(
            conversation_id,
            "user",
            message,
        )
        increment_conversation_count(conversation_id)

    @staticmethod
    def save_ai_message(conversation_id, message):
        save_message(
            conversation_id,
            "ai",
            message,
        )
        increment_conversation_count(conversation_id)

    @staticmethod
    def get_history(conversation_id, limit=20):
        return get_recent_messages(
            conversation_id,
            limit=limit,
        )