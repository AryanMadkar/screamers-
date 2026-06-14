from database.lead_model import get_lead, update_lead, create_lead, log_extraction
from onboarding.step_config import STEPS, STEP_CONFIG, TRANSITION_PROMPTS, OFFICE_ADDRESS
from onboarding.extractor import extract_for_step
from onboarding.transition_generator import generate_transition

def handle_onboarding(conversation_id: str, user_id: str, user_message: str):
    """
    Turn-by-turn onboarding. One step per exchange.

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

    current_step = lead.get("onboarding_step", "intent")

    # ── Extract the field for this step ──
    extracted = extract_for_step(current_step, user_message)
    log_extraction(conversation_id, user_message, extracted)

    value = extracted.get("value")
    confidence = extracted.get("confidence", "low")
    config = STEP_CONFIG[current_step]

    # ── Validate extraction ──
    is_valid = config["validate"](value) if value is not None else False

    if not is_valid or confidence == "low":
        # Couldn't understand — re-ask naturally
        if confidence == "low" and value is not None:
            # Got something but not sure — confirm it
            reply = f"Just to confirm — did you mean **{extracted.get('raw_understood', value)}**? Could you say that again?"
          # Wait, in the original code, this line had a tiny formatting typo: extracted.get('raw_understood', value)
          # which is correct, but let's make sure it's valid.
        else:
            reply = config["clarify_prompt"]
        return False, reply

    # ── Valid extraction — save it ──
    field = config["field"]
    next_step_index = STEPS.index(current_step) + 1

    updates = {
        field: value,
    }

    # ── Check if this was the last step ──
    if next_step_index >= len(STEPS):
        updates["onboarding_step"] = "done"
        update_lead(conversation_id, updates)

        # Closing confirmation
        name = lead.get("name") or value  # name might have just been collected
        intent = lead.get("intent", "")
        location = lead.get("location", "")
        meeting = value if current_step == "meeting" else lead.get("meeting_time", "")

        closing = (
            f"Thank you, {name}! 🎉 You're all set. "
            f"We've noted that you're looking to {intent} in {location}. "
            f"{'We look forward to meeting you at ' + meeting + '!' if meeting and meeting != 'not available' else 'We will reach out to schedule a suitable time.'} "
            f"Our office is at {OFFICE_ADDRESS}. Is there anything else I can help you with?"
        )
        return False, closing  # Next call will return True

    # ── Move to next step ──
    next_step = STEPS[next_step_index]
    updates["onboarding_step"] = next_step
    update_lead(conversation_id, updates)

    # Generate natural transition to next question
    updated_lead = {**lead, **updates}
    reply = generate_transition(updated_lead, next_step)

    return False, reply