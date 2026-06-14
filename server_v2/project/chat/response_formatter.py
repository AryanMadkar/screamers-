class ResponseFormatter:
    @staticmethod
    def format(user_id, conversation_id, message, response):
        return {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "message": message,
            "response": response,
        }
