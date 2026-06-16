import uuid
from datetime import datetime
from models.conversation import Conversation
from models.call_state import CallState
from models.real_estate import RealEstateMemory

class CallSession:
    def __init__(self):
        self.call_id = str(uuid.uuid4())
        self.conversation = Conversation()
        self.language = 'unknown'          # detected STT language
        self.preferred_language = 'english'  # caller-chosen language: 'english' | 'hindi'
        self.current_chunk = None
        self.chunk_queue = []
        self.current_text = ""
        # Rich transcript object populated by STT stage.
        # Carries text + metadata so downstream stages never need to re-parse.
        self.current_transcript = {
            "text": "",
            "language": "unknown",
            "confidence": 0.0,
            "timestamp": None,
        }
        self.ai_response = ""
        self.ai_response_ssml = ""
        self.active = True
        self.processing = False
        self.memory = RealEstateMemory()
        self.next_action = None
        self.context = ""
        self.state = CallState.IDLE

    def to_dict(self):
        return {
            'call_id': self.call_id,
            'language': self.language,
            'preferred_language': self.preferred_language,
            'current_text': self.current_text,
            'current_transcript': self.current_transcript,
            'ai_response': self.ai_response,
            'ai_response_ssml': self.ai_response_ssml,
            'active': self.active,
            'memory': self.memory.to_dict(),
            'context': self.context,
            'messages': self.conversation.get_messages(),
            'state': self.state.value,
        }

    def end_call(self):
        self.active = False
        self.set_state(CallState.ENDED)
        try:
            from database.mongodb import DatabaseService
            DatabaseService.save_completed_call(self)
        except Exception as e:
            print(f"[CallSession] Error saving completed call to MongoDB: {e}")

    def set_state(self, new_state):
        self.state = new_state

    def is_idle(self):
        return self.state == CallState.IDLE

    def is_listening(self):
        return self.state == CallState.LISTENING

    def is_transcribing(self):
        return self.state == CallState.TRANSCRIBING

    def is_thinking(self):
        return self.state == CallState.THINKING

    def is_speaking(self):
        return self.state == CallState.SPEAKING

    def is_ended(self):
        return self.state == CallState.ENDED