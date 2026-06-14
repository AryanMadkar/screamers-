from onboarding.step_config import (
    OFFICE_ADDRESS, STEPS, STEP_FIELDS, VALIDATORS,
    CLARIFY_PROMPTS, TRANSITION_PROMPTS, OPTIONAL_FIELD_MAP,
)
from onboarding.extractor import extract_lead_fields
from onboarding.transition_generator import generate_transition
from database.lead_model import get_lead, update_lead, create_lead, log_extraction
from chat.message_manager import MessageManager


def handle_onboarding(conversation_id: str, user_id: str, user_message: str):
    """
    Greedy multi-field onboarding with dynamic step skipping.

    Returns:
        (onboarding_complete: bool, reply: str | None)
    """
    lead = get_lead(conversation_id)

    # ── Brand new user: create lead and send welcome ──
    if lead is None:
        create_lead(conversation_id, user_id)
        welcome = (
            "👋 Hey there! I'm Priya, your personal real estate guide. "
            "I'm here to help you find your perfect property in India! "
            "To get started — are you looking to **buy** or **rent** a place?"
        )
        return False, welcome

    # ── Restart/Reset check ──
    clean_msg = user_message.strip().lower()
    if clean_msg in ("restart", "start over", "reset"):
        reset_fields = {
            "name": None,
            "contact_number": None,
            "intent": None,
            "location": None,
            "bhk": None,
            "property_type": None,
            "budget": None,
            "furnished": None,
            "area_sqft": None,
            "facing": None,
            "floor_preference": None,
            "possession": None,
            "amenities": None,
            "meeting_time": None,
            "onboarding_step": "intent",
            "clarification_retries": 0
        }
        update_lead(conversation_id, reset_fields)
        
        # Clear message history so extractor doesn't read old turns
        from database.db import message_collection
        message_collection.delete_many({"conversation_id": conversation_id})
        
        welcome = (
            "👋 No problem! Let's start fresh. Are you looking to **buy** or **rent** a property?"
        )
        return False, welcome

    # ── Explicit Cancel/Stop check ──
    if clean_msg in ("stop", "cancel", "nevermind", "exit"):
        update_lead(conversation_id, {"onboarding_step": "abandoned"})
        disengage_msg = (
            "No worries! I've paused our chat. If you change your mind and want to find a property "
            "later, just type 'restart' or 'start over' anytime. Have a great day!"
        )
        return False, disengage_msg

    # ── Already finished onboarding or abandoned ──
    current_step = lead.get("onboarding_step")
    if current_step == "done":
        return True, None

    if current_step == "abandoned":
        return False, "I've paused our conversation. If you'd like to start over or look for properties, just type 'restart'!"

    # ── Build full conversation history for context ──
    history = MessageManager.get_history(conversation_id, limit=40)
    history_text = "\n".join(
        f"{msg['sender'].capitalize()}: {msg['content']}" for msg in history
    )

    # ── Greedy: extract ALL fields from history in one LLM call ──
    extracted = extract_lead_fields(history_text)
    log_extraction(conversation_id, user_message, extracted)

    # ── Save any newly valid REQUIRED fields ──
    updates = {}
    for step in STEPS:
        field = STEP_FIELDS[step]
        val = extracted.get(field)
        if val is not None and VALIDATORS[step](val):
            if lead.get(field) != val:
                updates[field] = val

    # ── Save any newly valid OPTIONAL fields (greedy bonus collection) ──
    for extract_key, (db_field, validator) in OPTIONAL_FIELD_MAP.items():
        val = extracted.get(extract_key)
        if val is not None and validator(val):
            if lead.get(db_field) != val:
                updates[db_field] = val

    if updates:
        update_lead(conversation_id, updates)
        lead = {**lead, **updates}

    # ── Determine the next unfilled REQUIRED step ──
    next_step = None
    for step in STEPS:
        field = STEP_FIELDS[step]
        val = lead.get(field)
        if val is None or not VALIDATORS[step](val):
            next_step = step
            break

    # ── All required steps filled → onboarding done ──
    if next_step is None:
        update_lead(conversation_id, {"onboarding_step": "done"})

        name = lead.get("name") or "there"
        intent = lead.get("intent", "")
        location = lead.get("location", "")
        bhk = lead.get("bhk", "")
        budget = lead.get("budget", "")
        meeting = lead.get("meeting_time", "")

        closing = (
            f"That's all I need, {name}! 🎉 We've got everything noted — "
            f"you're looking to {intent} a {bhk} in {location}"
            f"{' within ' + budget if budget else ''}. "
            f"{'We look forward to meeting you at ' + meeting + '!' if meeting and meeting != 'not available' else 'Our team will reach out to schedule a suitable time.'} "
            f"Our office is at {OFFICE_ADDRESS}. "
            f"Meanwhile, feel free to ask me anything about the property market — I can search listings for you too! 🏡"
        )
        return False, closing

    # ── Step progressed? → generate natural LLM transition ──
    previous_step = lead.get("onboarding_step", "intent")

    if next_step != previous_step:
        update_lead(conversation_id, {
            "onboarding_step": next_step,
            "clarification_retries": 0
        })
        lead["onboarding_step"] = next_step
        lead["clarification_retries"] = 0
        reply = generate_transition(lead, next_step)
        return False, reply

    # ── Step unchanged → user didn't answer current question ──
    retries = lead.get("clarification_retries", 0) + 1
    if retries >= 3:
        update_lead(conversation_id, {
            "onboarding_step": "abandoned",
            "clarification_retries": retries
        })
        disengage_msg = (
            "I see we're having some trouble getting the details for this step. "
            "To avoid taking up more of your time, I'll stop here. "
            "If you'd like to try again later, just type 'restart' or 'start over' to begin again!"
        )
        return False, disengage_msg

    update_lead(conversation_id, {"clarification_retries": retries})
    return False, CLARIFY_PROMPTS[next_step]