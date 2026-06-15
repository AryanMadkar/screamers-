import uuid
from datetime import datetime
from models.conversation import Conversation
from models.call_state import CallState


class CallSession:
    def __init__(self):
        self.call_id = str(uuid.uuid4())
        self.conversation = Conversation()
        self.language = 'unknown'
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
        self.active = True
        self.processing = False
        self.memory = {}
        self.context = ""
        self.state = CallState.IDLE

    def to_dict(self):
        return {
            'call_id': self.call_id,
            'language': self.language,
            'current_text': self.current_text,
            'current_transcript': self.current_transcript,
            'ai_response': self.ai_response,
            'active': self.active,
            'memory': self.memory,
            'context': self.context,
            'messages': self.conversation.get_messages(),
            'state': self.state.value,
        }

    def end_call(self):
        self.active = False
        self.set_state(CallState.ENDED)

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