import json
import re
from onboarding.step_config import EXTRACTION_SYSTEM_PROMPT


def extract_json(text: str) -> str:
    """Robustly finds the first complete JSON block {...} in any text."""
    # Try to find outermost braces
    start = text.find('{')
    if start == -1:
        return text
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return text[start:]


def extract_lead_fields(history_text: str) -> dict:
    """
    Calls Groq with full conversation history to greedily extract
    all 14 lead fields in a single LLM call.
    """
    from services.llm import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    EMPTY = {
        "intent": None, "location": None, "bhk": None,
        "budget": None, "name": None, "contact_number": None,
        "meeting_time": None, "property_type": None,
        "furnished": None, "area_sqft": None, "facing": None,
        "floor_preference": None, "possession": None, "amenities": None,
    }

    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(content=f"Conversation history:\n\n{history_text}\n\nExtract lead details now.")
        ])
        raw = response.content.strip()

        # Strip any markdown fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)

        json_str = extract_json(raw)
        parsed = json.loads(json_str.strip())

        # Normalise — guarantee all keys exist
        result = {k: parsed.get(k) for k in EMPTY}
        return result

    except Exception as e:
        result = dict(EMPTY)
        result["_error"] = str(e)
        return result
