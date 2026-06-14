from database.conversation_model import (
    create_conversation,
    get_active_conversations,
)

class ConversationManager:
    @staticmethod
    def resolve_conversation(user_id, conversation_id=None):
        """
        Resolve conversation.

        Returns:
            conversation_id
        """
        if conversation_id is None:
            return create_conversation(user_id)

        conversations = get_active_conversations(user_id)

        for conv in conversations:
            if conv["conversation_id"] == conversation_id:
                return conversation_id

        return create_conversation(user_id)