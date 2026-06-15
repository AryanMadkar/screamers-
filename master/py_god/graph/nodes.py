from services.stt_service import STTService
from models.call_session import CallSession

stt = STTService()

def speech_to_text_node(state: CallSession):
    try:
        if not state.current_chunk or not state.current_chunk.file_path:
            raise Exception("No current audio chunk file path available in state")
            
        text = stt.transcribe(state.current_chunk.file_path)
        state.conversation.add_user(text)
        state.current_text = text
        return state
    except Exception as e:
        raise Exception(f"Error in speech_to_text_node: {e}")
    
def language_detection_node(state: CallSession):
    try:
        text = state.current_text.strip().lower()
        if "hindi" in text or "हिंदी" in text:
            state.language = "hindi"
        elif "english" in text:
            state.language = "english"
        else:
            state.language = "unknown"
        return state
    except Exception as e:
        raise Exception(f"Error in language_detection_node: {str(e)}")