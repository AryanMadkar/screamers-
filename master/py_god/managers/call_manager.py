from models.call_session import CallSession


class CallManager:
    def __init__(self):
        self.calls = {}
    def create_call(self):
        call = CallSession(caller_id=None, callee_id=None)
        self.calls[call.call_id] = call
        return call
    
    def get_call(self, call_id):
        return self.calls.get(call_id)
    
    def end_call(self, call_id):
        if call_id in self.calls:
            self.calls[call_id].end_call()
            del self.calls[call_id]