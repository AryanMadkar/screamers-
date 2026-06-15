from services.stt_service import STTService


stt = STTService()


def speech_to_text_node(state):
    try:
        
        text = stt.transcribe(state["audio_path"])

        state["text"] = text

        return state
    except Exception as e:

        raise Exception(f"Error in speech_to_text_node: {str(e)}")