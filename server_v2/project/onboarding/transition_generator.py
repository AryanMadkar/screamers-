from onboarding.step_config import OFFICE_ADDRESS

TRANSITION_SYSTEM_PROMPT = """
You are Priya — a warm, witty, and knowledgeable real estate consultant at a top Indian real estate agency.
You are chatting with a potential buyer or renter over WhatsApp/web.

Your personality:
- Friendly and empathetic, like a trusted friend who happens to know real estate very well
- Never robotic, never generic. React to what the user actually said
- Use casual Indian English naturally — words like "absolutely", "sure thing", "great choice!", "no worries"
- Keep responses SHORT: one warm acknowledgment + one focused question
- Use light emojis occasionally (🏡 🙌 👌) but don't overdo it
- Never repeat back everything the user said mechanically
- If the user shared something personal (budget, location), acknowledge it warmly before asking next

Do NOT ask about things already known. Do NOT list multiple questions at once.
"""

QUESTIONS = {
    "location":  "Which city or area are you looking in?",
    "bhk":       "How many bedrooms are you thinking — 1BHK, 2BHK, 3BHK?",
    "budget":    "What's the budget range you have in mind?",
    "name":      "And your name?",
    "contact":   "Could I get your contact number so our team can reach out?",
    "meeting":   f"When would you be free for a quick call or visit? We're at {OFFICE_ADDRESS}.",
}


def generate_transition(lead: dict, next_step: str) -> str:
    """
    Generates a natural, human-sounding transition to the next onboarding question.
    Falls back to a static question if LLM fails.
    """
    from services.llm import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    question = QUESTIONS.get(next_step, "Could you tell me a bit more?")

    # Build what we know so far as context
    known_parts = []
    if lead.get("intent"):    known_parts.append(f"intent: {lead['intent']}")
    if lead.get("location"):  known_parts.append(f"location: {lead['location']}")
    if lead.get("bhk"):       known_parts.append(f"bhk: {lead['bhk']}")
    if lead.get("budget"):    known_parts.append(f"budget: {lead['budget']}")
    if lead.get("name"):      known_parts.append(f"name: {lead['name']}")
    if lead.get("property_type"): known_parts.append(f"property type: {lead['property_type']}")
    if lead.get("furnished"):     known_parts.append(f"furnished: {lead['furnished']}")
    if lead.get("possession"):    known_parts.append(f"possession: {lead['possession']}")

    context = (
        f"What we know so far: {', '.join(known_parts) if known_parts else 'just started'}\n\n"
        f"Next thing to ask: \"{question}\"\n\n"
        f"Write a single natural, warm message that briefly acknowledges what was just shared "
        f"(if relevant) and asks the next question. Max 2 sentences. Sound human."
    )

    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(content=TRANSITION_SYSTEM_PROMPT),
            HumanMessage(content=context),
        ])
        return response.content.strip()
    except Exception:
        return question
