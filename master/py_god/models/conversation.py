from models.message import Message

class Conversation:
    def __init__(self):
        self.messages = []
        
    def add_user(self,text:str):
        self.messages.append(Message(role='user',content=text))
        
    def add_ai(self,text:str):
        self.messages.append(Message(role='assistant',content=text))
        
    def get_messages(self):
        return [msg.to_dict() for msg in self.messages]
    
    def last_message(self):
        if self.messages:
            return self.messages[-1]
        return None