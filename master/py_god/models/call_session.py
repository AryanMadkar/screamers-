import uuid
from models.conversation import Conversation
class CallSession:
    def __init__(self, caller_id, callee_id):
        self.call_id = str(uuid.uuid4())
        self.language = 'unknown'
        self.conversation = Conversation()
        self.active = True
        self.context = ""
        self.memory = {}
        self.user_text = ""
        self.ai_text = ""
        
    def to_dict(self):
        return {
            'call_id': self.call_id,
            'language': self.language,
            'active': self.active,
            'messages': self.conversation.get_messages(),
        }
        
    def end_call(self):
        self.active = False