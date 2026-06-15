from datetime import datetime

class Message:
    def  __init__(self,role:str,content:str):
        self.role = role
        self.content = content
        self.timestamp = datetime.now()
        
    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }