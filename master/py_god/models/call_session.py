import uuid
from models.conversation import Conversation

class CallSession:
    def __init__(self):
        self.call_id = str(uuid.uuid4())
        self.conversation = Conversation()
        self.language = 'unknown'
        self.current_chunk = None
        self.chunk_queue = []
        self.current_text = ""
        self.ai_response = ""
        self.active = True
        self.memory = {}
        self.context = ""
        self.processing = False
        
    def to_dict(self):
        return {
            'call_id': self.call_id,
            'language': self.language,
            'current_text': self.current_text,
            'ai_response': self.ai_response,
            'active': self.active,
            'memory': self.memory,
            'context': self.context,
            'messages': self.conversation.get_messages(),
        }
        
    def end_call(self):
        self.active = False