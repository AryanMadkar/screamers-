from memory.memory_extractor import MemoryExtractor
class MemoryStage:
    def __init__(self):
        self.extractor = MemoryExtractor()

    def process(self, call_session):

        # Future Memory Extraction

        call_session = self.extractor.extract(call_session)

        return call_session