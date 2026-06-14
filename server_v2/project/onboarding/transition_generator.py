from onboarding.step_config import OFFICE_ADDRESS

TRANSITION_SYSTEM_PROMPT = """
You are Priya, a warm real estate consultant. 
You just collected one piece of info from the user and now need to naturally ask the next question.
Keep it SHORT — one sentence acknowledgment + one question. Sound human, not robotic.
Do not list options. Do not give long explanations.
"""

def generate_transition(lead: dict, next_step: str) -> str:
    """LLM generates a natural bridge from what was just said to the next question."""
    from services.llm import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    questions = {
        "location": "Which city or area are you looking for a property in?",
        "name":     "May I know your name?",
        "amenities": "Do you have any specific requirements — like number of rooms, parking, or any amenities you'd prefer?",
        "meeting":  f"Would you be available to meet us or visit our office? We're at {OFFICE_ADDRESS}. What time works for you?"
    }

    # Build context of what we know so far
    known = []
    if lead.get("intent"):    known.append(f"intent: {lead['intent']}")
    if lead.get("location"):  known.append(f"location: {lead['location']}")
    if lead.get("name"):      known.append(f"name: {lead['name']}")
    if lead.get("amenities"): known.append(f"amenities: {lead['amenities']}")

    context = f"""
What we know so far: {', '.join(known) if known else 'nothing yet'}
Next question to ask: "{questions[next_step]}"

Write one natural, warm sentence that acknowledges what they just said (if relevant) and asks the next question.
Keep it under 2 sentences. Sound like a real consultant, not a chatbot.
"""

    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(content=TRANSITION_SYSTEM_PROMPT),
            HumanMessage(content=context)
        ])
        return response.content.strip()
    except Exception:
        # Fallback to static question if LLM fails
        return questions[next_step]
