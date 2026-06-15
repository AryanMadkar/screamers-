from flow.conversation_flow import ConversationFlow
from agent.agent_action import AgentAction
class ContextStage:

    def __init__(self):
        self.flow = ConversationFlow()

    def process(self, call_session):
        if call_session.next_action != AgentAction.ASK:
            return call_session
        
        question = self.flow.next_question(call_session)
        call_session.context = question
        # Future Context Builder

        return call_session