import json
import re
from onboarding.step_config import EXTRACTION_SYSTEM_PROMPT

def extract_json(text: str) -> str:
    """Finds and extracts the first JSON block {...} from text."""
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

def extract_lead_fields(history_text: str) -> dict:
    """Calls Groq to extract all lead fields from the conversation history."""
    from services.llm import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(content=f"Extract lead details from the following conversation history:\n\n{history_text}")
        ])
        raw = response.content.strip()

        # Isolate JSON content
        json_str = extract_json(raw)
        
        # Clean up any potential markdown fences
        json_str = re.sub(r"^```(?:json)?", "", json_str, flags=re.MULTILINE)
        json_str = re.sub(r"```$", "", json_str, flags=re.MULTILINE)

        parsed = json.loads(json_str.strip())
        
        # Normalize parsed output to guarantee all keys are present
        normalized = {
            "intent": parsed.get("intent"),
            "location": parsed.get("location"),
            "name": parsed.get("name"),
            "amenities": parsed.get("amenities"),
            "meeting_time": parsed.get("meeting_time")
        }
        return normalized

    except Exception as e:
        return {
            "intent": None,
            "location": None,
            "name": None,
            "amenities": None,
            "meeting_time": None,
            "error": str(e)
        }
