from groq import Groq
from config import Config

class STTService:

    def __init__(self):

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

    def transcribe(self, audio_path)-> str:
        try:
                
            with open(audio_path, "rb") as file:

                transcription = self.client.audio.transcriptions.create(
                    file=file,
                    model=Config.MODEL_NAME
                )

            return transcription.text
        except Exception as e:
            raise Exception(f"Error in STTService.transcribe: {str(e)}")