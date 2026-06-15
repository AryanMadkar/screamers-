from groq import Groq
from config import Config
from services.stt.base_stt import BaseSTT


class GroqSTT(BaseSTT):
    def __init__(self):
        self.groq = Groq(api_key=Config.GROQ_API_KEY)

    def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe the given audio file to text using the Groq Whisper API.

        Raises:
            Exception: Re-raises any API or I/O errors so callers can handle them.
                       Never silently returns "" — an empty result means the caller
                       cannot tell whether STT failed or the audio was genuinely silent.
        """
        with open(audio_file_path, 'rb') as audio_file:
            transcription = self.groq.audio.translations.create(
                file=audio_file,
                model=Config.GROQ_MODEL,
            )
        return transcription.text