from agent.decision_engine import DecisionEngine

class DecisionStage:
    
    def __init__(self):
        self.engine = DecisionEngine()
    
    def process(self, call_session):
        call_session.next_action = self.engine.decide(call_session)
        return call_session