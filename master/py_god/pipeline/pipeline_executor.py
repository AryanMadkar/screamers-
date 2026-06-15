from pipeline.stages.stt_stage import STTStage
from pipeline.stages.memory_stage import MemoryStage
from pipeline.stages.context_stage import ContextStage
from pipeline.stages.ai_stage import AIStage
from pipeline.stages.tts_stage import TTSStage


class PipelineExecutor:
    def __init__(self):

        self.stt = STTStage()
        self.memory = MemoryStage()
        self.context = ContextStage()
        self.ai = AIStage()
        self.tts = TTSStage()

    def execute(self, call_session):
        try:
            
            call_session = self.stt.process(call_session)

            call_session = self.memory.process(call_session)

            call_session = self.context.process(call_session)

            call_session = self.ai.process(call_session)

            call_session = self.tts.process(call_session)

            return call_session
        except Exception as e:
            print(f"Pipeline execution error: {e}")
            return call_session