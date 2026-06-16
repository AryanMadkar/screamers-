from models.call_state import CallState
from pipeline.stages.stt_stage import STTStage
from pipeline.stages.agent_stage import AgentStage
from pipeline.stages.tts_stage import TTSStage


class PipelineExecutor:
    def __init__(self):
        self.stt = STTStage()
        self.agent = AgentStage()
        self.tts = TTSStage()

    def execute(self, session):
        """
        Run the full pipeline sequentially, advancing call state at each phase.

        State transitions owned here:
            TRANSCRIBING  (set by worker before calling execute)
              └─ STTStage        : transcribe audio → text
            THINKING      (set here before AI phases)
              └─ AgentStage      : execute LLM reasoning, extract facts, update memory, plan action
            SPEAKING      (set here before TTS)
              └─ TTSStage        : synthesise speech and apply SpeechFormatter
            IDLE          (set by worker after execute returns)

        Exceptions are intentionally NOT caught here — the worker owns error
        recovery and state reset, so failures propagate up to it.
        """
        # Phase 1 — already TRANSCRIBING (set by worker)
        session = self.stt.process(session)

        # Phase 2 — THINKING: memory retrieval, context building, AI inference
        session.set_state(CallState.THINKING)
        session = self.agent.process(session)

        # Phase 3 — SPEAKING: text-to-speech synthesis
        session.set_state(CallState.SPEAKING)
        session = self.tts.process(session)

        return session