from chat.user_manager import UserManager
from chat.conversation_manager import ConversationManager
from chat.message_manager import MessageManager

from chat.context_builder import ContextBuilder
from chat.response_formatter import ResponseFormatter
from chat.onboarding_handler import OnboardingHandler
from services.llm import generate_response
from database.lead_model import get_lead, update_lead
from database.conversation_model import end_conversation


class ChatService:
    @staticmethod
    def chat(user_id, conversation_id, message):
        # --- Resolve user ---
        user_id = UserManager.resolve_user(user_id)

        # --- Handle restart early: reactivate ended session rather than creating new ---
        clean_msg_early = message.strip().lower()
        if clean_msg_early in ("restart", "start over", "reset") and conversation_id:
            from database.conversation_model import conversations_collection
            from database.db import message_collection
            existing = conversations_collection.find_one({"conversation_id": conversation_id})
            if existing and existing.get("status") == "ended":
                # Reactivate the conversation
                conversations_collection.update_one(
                    {"conversation_id": conversation_id},
                    {"$set": {"status": "active", "ended_at": None}}
                )
                # Clear message history so extractor starts fresh
                message_collection.delete_many({"conversation_id": conversation_id})
                # Reset the lead fields
                reset_fields = {
                    "name": None, "contact_number": None, "intent": None,
                    "location": None, "bhk": None, "property_type": None,
                    "budget": None, "furnished": None, "area_sqft": None,
                    "facing": None, "floor_preference": None, "possession": None,
                    "amenities": None, "meeting_time": None,
                    "onboarding_step": "intent", "clarification_retries": 0
                }
                update_lead(conversation_id, reset_fields)
                welcome = "👋 No problem! Let's start fresh. Are you looking to **buy** or **rent** a property?"
                MessageManager.save_user_message(conversation_id, message)
                MessageManager.save_ai_message(conversation_id, welcome)
                return ResponseFormatter.format(user_id, conversation_id, message, welcome)

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
            end_conversation(conversation_id)
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

        # --- Check if LLM requested conversation ending ---
        if "[END_CONVERSATION]" in ai_response:
            ai_response = ai_response.replace("[END_CONVERSATION]", "").strip()
            end_conversation(conversation_id)

        # --- Save AI response ---
        MessageManager.save_ai_message(conversation_id, ai_response)

        return ResponseFormatter.format(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            response=ai_response
        )