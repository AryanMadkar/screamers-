from services.speech_formatter import SpeechFormatter

class TTSStage:

    def process(self, call_session):
        if call_session.ai_response:
            lang = getattr(call_session, "preferred_language", "english")
            call_session.ai_response_ssml = SpeechFormatter.format_speech(
                call_session.ai_response,
                language=lang
            )
        return call_session