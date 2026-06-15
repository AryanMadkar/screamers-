from services.stt_service import STTService


stt = STTService()


def speech_to_text_node(state):

    try:
        text = stt.transcribe(state["audio_path"])

        state["messages"].append({
            "role": "user",
            "content": text
        })

        state["current_text"] = text

        return state

    except Exception as e:
        raise Exception(
            f"Error in speech_to_text_node: {e}"
        )
    
    
def language_detection_node(state):
    try:
        text = state["current_text"].strip().lower()
        if "hindi" in text or "हिंदी" in text:
            state["language"] = "hindi"

        elif "english" in text:
            state["language"] = "english"

        else:
            state["language"] = "unknown"

        return state
    except Exception as e:
        raise Exception(f"Error in language_detection_node: {str(e)}")