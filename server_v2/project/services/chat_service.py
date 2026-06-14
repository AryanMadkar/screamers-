from database.user_model import user_exists, update_last_seen, create_user
from database.conversation_model import (
    create_conversation,
    get_active_conversations,
    increment_conversation_count,  # FIX: was wrongly imported from db.py
)
from database.message_model import save_message, get_recent_messages  # FIX: correct import source
from services.llm import generate_response


def chat(user_id, conversation_id, message):
    # --- Resolve user ---
    if user_id is None or not user_exists(user_id):
        # FIX: original code had two separate branches but both needed create_user;
        # merged into one clean check
        user_id = create_user()
    else:
        update_last_seen(user_id)

    # --- Resolve conversation ---
    if conversation_id is None:
        conversation_id = create_conversation(user_id)
    else:
        # FIX: original had typo `conversationn` and never validated the conversation exists
        active = get_active_conversations(user_id)
        matched = next(
            (c for c in active if c["conversation_id"] == conversation_id),
            None
        )
        if matched is None:
            # Conversation not found or not active — start a new one
            conversation_id = create_conversation(user_id)

    # --- Save user message ---
    # FIX: original called save_message with 4 args; correct signature is 3
    save_message(conversation_id, "user", message)
    increment_conversation_count(conversation_id)

    # --- Build history and call LLM ---
    history = get_recent_messages(conversation_id, limit=20)
    llm_input = ""
    for msg in history:
        llm_input += f"{msg['sender']}: {msg['content']}\n"

    ai_response = generate_response(llm_input)

    # --- Save AI response ---
    save_message(conversation_id, "ai", ai_response)
    increment_conversation_count(conversation_id)

    return {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "message": message,
        "response": ai_response
    }
