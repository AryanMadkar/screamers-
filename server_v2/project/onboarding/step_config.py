from onboarding.validator import (
    validate_intent,
    validate_location,
    validate_name,
    validate_amenities,
    validate_meeting
)

OFFICE_ADDRESS = "123 Prestige Tower, Bandra West, Mumbai - 400050"

STEPS = ["intent", "location", "name", "amenities", "meeting"]

STEP_FIELDS = {
    "intent": "intent",
    "location": "location",
    "name": "name",
    "amenities": "amenities",
    "meeting": "meeting_time"
}

VALIDATORS = {
    "intent": validate_intent,
    "location": validate_location,
    "name": validate_name,
    "amenities": validate_amenities,
    "meeting": validate_meeting
}

CLARIFY_PROMPTS = {
    "intent": "Sorry, I didn't quite catch that! Are you looking to **buy** a property or **rent** one?",
    "location": "Could you tell me which city or area you have in mind? For example — South Mumbai, Pune, Thane?",
    "name": "I didn't catch your name! Could you tell me what to call you?",
    "amenities": "Do you have any specific requirements? Like number of rooms, parking, gym — or any area preferences? You can say 'none' if you're flexible!",
    "meeting": f"Would you be available to visit our office or have a quick call with us? Our office is at {OFFICE_ADDRESS}. What time works for you?"
}

EXTRACTION_SYSTEM_PROMPT = """
You are a precise data extraction assistant for a real estate agency.
Analyze the provided conversation history and extract the following lead details:
1. intent: Must be exactly "buy" or "rent".
2. location: The city, area, or neighborhood they want (e.g. "Malad, Mumbai", "Pune").
3. name: The user's name. Strip filler words (e.g., "my name is", "call me"). Title-case it.
4. amenities: A clean summary of their requirements (e.g. "2BHK, parking", "pool, gym"). If they say none or don't care, set it to "none".
5. meeting_time: A normalised meeting time in plain English (e.g., "Saturday 3pm", "tomorrow evening"). If they refuse or say no, set it to "not available".

Return ONLY valid JSON in this format, with no markdown formatting and no conversational text:
{{
  "intent": "buy" | "rent" | null,
  "location": "string" | null,
  "name": "string" | null,
  "amenities": "string" | null,
  "meeting_time": "string" | null
}}

Rules:
- Do not guess fields that are not explicitly stated or implied by the conversation.
- If a field is not present or unclear, set it to null.
- Extract any new details provided in the latest messages.
"""

TRANSITION_PROMPTS = {
    "intent": "Are you looking to **buy** or **rent** a property?",
    "location": None,
    "name": None,
    "amenities": None,
    "meeting": None,
}
