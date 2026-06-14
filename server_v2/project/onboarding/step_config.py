from onboarding.validator import (
    validate_intent,
    validate_location,
    validate_name,
    validate_amenities,
    validate_meeting
)

OFFICE_ADDRESS = "123 Prestige Tower, Bandra West, Mumbai - 400050"

STEPS = ["intent", "location", "name", "amenities", "meeting"]

STEP_CONFIG = {
    "intent": {
        "field": "intent",
        "extraction_prompt": """
The user was asked whether they want to buy or rent a property.
Extract their intent from their reply.

User said: "{message}"

Return ONLY valid JSON:
{{
  "value": "buy" | "rent" | null,
  "confidence": "high" | "low",
  "raw_understood": "what you think they meant in plain english"
}}

Rules:
- buy/purchase/kharidna/lena → "buy"
- rent/lease/kiraye/rental → "rent"  
- If completely unclear → null
- No markdown, no explanation, just JSON.
""",
        "validate": validate_intent,
        "clarify_prompt": "Sorry, I didn't quite catch that! Are you looking to **buy** a property or **rent** one?"
    },

    "location": {
        "field": "location",
        "extraction_prompt": """
The user was asked which city or area they are looking for a property in.
Extract the location from their reply.

User said: "{message}"

Return ONLY valid JSON:
{{
  "value": "extracted location as clean string" | null,
  "confidence": "high" | "low",
  "raw_understood": "what you think they meant"
}}

Rules:
- Clean up STT noise (e.g. "andheri west mumbai" is fine as-is)
- If they say something like "anywhere" or "not sure" → null with confidence low
- No markdown, no explanation, just JSON.
""",
        "validate": validate_location,
        "clarify_prompt": "Could you tell me which city or area you have in mind? For example — South Mumbai, Pune, Thane?"
    },

    "name": {
        "field": "name",
        "extraction_prompt": """
The user was asked for their name.
Extract their name from their reply.

User said: "{message}"

Return ONLY valid JSON:
{{
  "value": "their name, title-cased" | null,
  "confidence": "high" | "low",
  "raw_understood": "what you think they said"
}}

Rules:
- Extract just the name, strip filler ("my name is", "I am", "call me")
- If they give first + last, keep both
- If unclear or they said something unrelated → null
- No markdown, no explanation, just JSON.
""",
        "validate": validate_name,
        "clarify_prompt": "I didn't catch your name! Could you tell me what to call you?"
    },

    "amenities": {
        "field": "amenities",
        "extraction_prompt": """
The user was asked if they have any specific requirements or amenities in mind for the property.
Extract their preferences from their reply.

User said: "{message}"

Return ONLY valid JSON:
{{
  "value": "clean summary of requirements" | "none" | null,
  "confidence": "high" | "low",
  "raw_understood": "what you think they meant"
}}

Rules:
- If they say nothing specific / no / nahi / none / don't care → "none"
- Otherwise summarise what they want (e.g. "2BHK, parking, gym, near metro")
- If completely incoherent → null with low confidence
- No markdown, no explanation, just JSON.
""",
        "validate": validate_amenities,
        "clarify_prompt": "Do you have any specific requirements? Like number of rooms, parking, gym — or any area preferences? You can say 'none' if you're flexible!"
    },

    "meeting": {
        "field": "meeting_time",
        "extraction_prompt": """
The user was asked if they are available for a meeting and what time suits them.
Extract their availability from their reply.

User said: "{message}"

Return ONLY valid JSON:
{{
  "value": "normalised meeting time in plain english" | "not available" | null,
  "confidence": "high" | "low",
  "raw_understood": "what you think they meant"
}}

Rules:
- Normalise to readable format: "Saturday 3pm", "Tomorrow evening", "Weekdays after 6pm"
- If they say no / not interested / busy → "not available"
- If completely unclear → null
- No markdown, no explanation, just JSON.
""",
        "validate": validate_meeting,
        "clarify_prompt": f"Would you be available to visit our office or have a quick call with us? Our office is at {OFFICE_ADDRESS}. What time works for you?"
    }
}

TRANSITION_PROMPTS = {
    "intent": "Are you looking to **buy** or **rent** a property?",
    "location": None,
    "name": None,
    "amenities": None,
    "meeting": None,
}
