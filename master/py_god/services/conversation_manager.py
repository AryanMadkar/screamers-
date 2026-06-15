import uuid


class ConversationManager:

    @staticmethod
    def create_conversation():
        try:
            
            return str(uuid.uuid4())
        except Exception as e:
            raise Exception(f"Error in ConversationManager.create_conversation: {str(e)}")