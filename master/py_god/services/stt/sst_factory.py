from services.stt.groq_stt import GroqSTT

class STTFactory:
    @staticmethod
    def create() -> GroqSTT:
        return GroqSTT()