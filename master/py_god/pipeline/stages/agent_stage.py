from agent.agent_orchestrator import AgentOrchestrator

class AgentStage:
    def __init__(self):
        self.orchestrator = AgentOrchestrator()

    def process(self, session):
        """
        Execute the single Agent Orchestrator thinking and memory updates.
        """
        return self.orchestrator.run(session)
