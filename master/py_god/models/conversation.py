from models.message import Message

class Conversation:
    def __init__(self):
        self.messages = []
        
    def add_user(self,text:str):
        try:
            self.messages.append(Message(role='user',content=text))
        except Exception as e:
            print(f"Error adding user message: {e}")
        
    def add_ai(self,text:str):
        try:
            self.messages.append(Message(role='assistant',content=text))
        except Exception as e:
            print(f"Error adding AI message: {e}")

    def get_messages(self):
        try :
            return [msg.to_dict() for msg in self.messages]
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []

    def last_message(self):
        try :
            if self.messages:
                return self.messages[-1]
            return None
        except Exception as e:
            print(f"Error retrieving last message: {e}")
            return None