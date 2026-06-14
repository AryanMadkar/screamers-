
from chat.user_manager import UserManager
from chat.conversation_manager import ConversationManager
from chat.message_manager import MessageManager

from chat.context_builder import ContextBuilder
from chat.response_formatter import ResponseFormatter
from chat.onboarding_handler import OnboardingHandler
from services.llm import generate_response


class ChatService:
    @staticmethod
    def chat(user_id, conversation_id, message):
        # --- Resolve user ---
        user_id = UserManager.resolve_user(user_id)

        # --- Resolve conversation ---
        conversation_id = ConversationManager.resolve_conversation(user_id, conversation_id)

        # --- Save user message ---
        MessageManager.save_user_message(conversation_id, message)

        # --- Handle onboarding ---
        completed,onboarding_reply = OnboardingHandler.handle(conversation_id, user_id, message)
        if not completed :
            MessageManager.save_ai_message(conversation_id, onboarding_reply)
            return ResponseFormatter.format(user_id, conversation_id, message, onboarding_reply)


        # --- Build context and generate response ---
        context = ContextBuilder.build_context(conversation_id)
        ai_response = generate_response(context)

        # --- Save AI response ---
        MessageManager.save_ai_message(conversation_id, ai_response)

        return ResponseFormatter.format(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            response=ai_response
        )