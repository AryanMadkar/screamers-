from abc import ABC, abstractmethod

class BaseSTT(ABC):
    @abstractmethod
    def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe the given audio file to text.

        :param audio_file_path: Path to the audio file to be transcribed."""
        pass