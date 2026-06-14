from database.lead_model import get_lead, update_lead, create_lead, log_extraction
from onboarding.step_config import STEPS, STEP_FIELDS, VALIDATORS, CLARIFY_PROMPTS, TRANSITION_PROMPTS, OFFICE_ADDRESS
from onboarding.extractor import extract_lead_fields
from onboarding.transition_generator import generate_transition
from chat.message_manager import MessageManager

def handle_onboarding(conversation_id: str, user_id: str, user_message: str):
    """
    Greedy multi-field turn-by-turn onboarding.
    
    Returns:
        (onboarding_complete: bool, reply: str | None)
    """
    lead = get_lead(conversation_id)

    # ── Brand new user ──
    if lead is None:
        create_lead(conversation_id, user_id)
        # Welcome + first question
        welcome = (
            "👋 Hi! I'm Priya, your personal real estate consultant. "
            "Welcome! " + TRANSITION_PROMPTS["intent"]
        )
        return False, welcome

    # ── Onboarding already finished ──
    if lead.get("onboarding_step") == "done":
        return True, None

    # ── Build conversation history ──
    history = MessageManager.get_history(conversation_id, limit=30)
    history_text = "\n".join(f"{msg['sender'].capitalize()}: {msg['content']}" for msg in history)

    # ── Greedy extract fields from full history ──
    extracted = extract_lead_fields(history_text)
    log_extraction(conversation_id, user_message, extracted)

    # ── Filter and validate newly extracted values ──
    updates = {}
    for step in STEPS:
        field = STEP_FIELDS[step]
        extracted_val = extracted.get(field)
        
        # Validate the extracted value
        if extracted_val is not None and VALIDATORS[step](extracted_val):
            # Update if database doesn't have it, or user changes mind/corrects
            # For simplicity, we save any new valid value
            if lead.get(field) != extracted_val:
                updates[field] = extracted_val

    # Apply updates if any
    if updates:
        update_lead(conversation_id, updates)
        # Merge updates back into the local lead dict
        lead = {**lead, **updates}

    # ── Determine the next unfilled step ──
    next_step = None
    for step in STEPS:
        field = STEP_FIELDS[step]
        current_val = lead.get(field)
        if current_val is None or not VALIDATORS[step](current_val):
            next_step = step
            break

    # ── All steps filled ──
    if next_step is None:
        updates = {"onboarding_step": "done"}
        update_lead(conversation_id, updates)
        lead = {**lead, **updates}

        name = lead.get("name") or "there"
        intent = lead.get("intent", "")
        location = lead.get("location", "")
        meeting = lead.get("meeting_time", "")

        closing = (
            f"Thank you, {name}! 🎉 You're all set. "
            f"We've noted that you're looking to {intent} in {location}. "
            f"{'We look forward to meeting you at ' + meeting + '!' if meeting and meeting != 'not available' else 'We will reach out to schedule a suitable time.'} "
            f"Our office is at {OFFICE_ADDRESS}. Is there anything else I can help you with?"
        )
        return False, closing

    # ── Move to next step ──
    previous_step = lead.get("onboarding_step", "intent")
    
    if next_step != previous_step:
        # Step progressed! Save the new step state and generate transition
        update_lead(conversation_id, {"onboarding_step": next_step})
        lead["onboarding_step"] = next_step
        reply = generate_transition(lead, next_step)
        return False, reply
    else:
        # User reply did not provide the required details for the current step.
        # Fall back to the clarification prompt
        reply = CLARIFY_PROMPTS[next_step]
        return False, reply