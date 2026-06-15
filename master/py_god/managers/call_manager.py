from models.call_session import CallSession


class CallManager:
    def __init__(self):
        self.calls = {}
    def create_call(self):
        try:
            call = CallSession()
            self.calls[call.call_id] = call
            return call
        except Exception as e:
            print(f"Error creating call: {e}")
            return None

    def get_call(self, call_id):
        try:
            return self.calls.get(call_id)
        except Exception as e:
            print(f"Error retrieving call: {e}")
            return None

    def end_call(self, call_id):
        try:
            if call_id in self.calls:
                self.calls[call_id].end_call()
                del self.calls[call_id]
                return True
            return False
        except Exception as e:
            print(f"Error ending call: {e}")
            return False