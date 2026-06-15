from agent.agent_action import AgentAction

class DecisionEngine:
    
    def decide(self, call_session):
        memory = call_session.memory
        if memory.interested is False:
            return AgentAction.END
        if memory.complete():
            return AgentAction.SEARCH
        # Future Decision Logic
        return AgentAction.ASK