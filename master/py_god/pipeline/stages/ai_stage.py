from agent.agent_action import AgentAction
class AIStage:

    def process(self, call_session):
        if call_session.next_action == AgentAction.ASK:
            call_session.ai_response = call_session.context
        elif call_session.next_action == AgentAction.END:
            call_session.ai_response = "Thank you for your time. Goodbye!"
        elif call_session.next_action == AgentAction.SEARCH:
            call_session.ai_response = (
                "Great! I have collected your requirements. "
                "Let me search suitable properties for you."
            )
        else:
            call_session.ai_response = "I'm sorry, I didn't understand that."

        call_session.conversation.add_ai(call_session.ai_response)

        return call_session