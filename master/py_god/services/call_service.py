from services.session_service import call_manager

class CallService:
    @staticmethod
    def start_call():
        call = call_manager.create_call()
        return call.to_dict()
    @staticmethod
    def get_call(call_id):
        call = call_manager.get_call(call_id)
        if call:
            return call
        return None
    @staticmethod
    def end_call(call_id):
        return call_manager.end_call(call_id)