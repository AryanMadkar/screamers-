from chat.user_manager import UserManager
from chat.conversation_manager import ConversationManager
from chat.message_manager import MessageManager

from chat.context_builder import ContextBuilder
from chat.response_formatter import ResponseFormatter
from chat.onboarding_handler import OnboardingHandler
from services.llm import generate_response
from database.lead_model import get_lead


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
        completed, onboarding_reply = OnboardingHandler.handle(conversation_id, user_id, message)
        if not completed:
            MessageManager.save_ai_message(conversation_id, onboarding_reply)
            return ResponseFormatter.format(user_id, conversation_id, message, onboarding_reply)

        # --- Check for goodbye/disengagement in post-onboarding ---
        clean_msg = message.strip().lower().rstrip('.!?')
        goodbyes = ("bye", "goodbye", "thank you", "thanks", "thanks a lot", "thank you so much", "exit", "quit")
        if clean_msg in goodbyes or clean_msg.startswith(("thank you", "thanks", "bye")):
            goodbye_reply = (
                "You're very welcome! Glad I could help. If you ever need more assistance "
                "with properties, feel free to reach out. Have a wonderful day! 👋"
            )
            MessageManager.save_ai_message(conversation_id, goodbye_reply)
            return ResponseFormatter.format(
                user_id=user_id,
                conversation_id=conversation_id,
                message=message,
                response=goodbye_reply
            )

        # --- Build context and generate response ---
        lead = get_lead(conversation_id)
        context = ContextBuilder.build_context(conversation_id)
        ai_response = generate_response(context, lead)

        # --- Save AI response ---
        MessageManager.save_ai_message(conversation_id, ai_response)

        return ResponseFormatter.format(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            response=ai_response
        )