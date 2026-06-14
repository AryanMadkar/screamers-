import json
import re
from onboarding.step_config import STEP_CONFIG

def extract_for_step(step_key: str, user_message: str) -> dict:
    """Calls LLM to extract the field for the current step."""
    from services.llm import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    config = STEP_CONFIG[step_key]
    prompt = config["extraction_prompt"].format(message=user_message)

    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(content="You are a precise data extraction assistant. Return only valid JSON."),
            HumanMessage(content=prompt)
        ])
        raw = response.content.strip()

        # Strip markdown fences if model adds them
        raw = re.sub(r"^```(?:json)?", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"```$", "", raw, flags=re.MULTILINE)

        return json.loads(raw.strip())

    except Exception as e:
        return {
            "value": None,
            "confidence": "low",
            "raw_understood": f"extraction failed: {str(e)}"
        }
