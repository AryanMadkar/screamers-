from chat.message_manager import MessageManager

class ContextBuilder:
    @staticmethod
    def build_context(conversation_id, limit=20):
        history = MessageManager.get_history(conversation_id, limit=limit)
        return "\n".join(
            f"{msg['sender']}: {msg['content']}"
            for msg in history
        )