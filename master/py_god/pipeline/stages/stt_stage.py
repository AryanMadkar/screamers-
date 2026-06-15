from datetime import datetime

from models.call_state import CallState
from services.audio_service import AudioService
from services.stt.sst_factory import STTFactory


class STTStage:
    def __init__(self):
        self.stt = STTFactory.create()

    def process(self, session):
        """
        Step 6 & 7 — Transcribe audio → store text → persist to conversation → clean up file.

        Populates:
            session.current_text          – plain string for quick access
            session.current_transcript    – rich dict with text/language/confidence/timestamp
            session.conversation          – appends a 'user' message
        Cleans up:
            session.current_chunk temp file is deleted after successful transcription.
        """
        if session.current_chunk is None:
            return session

        # --- Transcribe ---
        text = self.stt.transcribe(session.current_chunk.file_path)
        # GroqSTT returns "" on error — treat it as a failure so we don't save blank messages
        if not text:
            raise RuntimeError("STT returned empty transcription — skipping chunk")

        # --- Step 6: Store text in session ---
        session.current_text = text

        # --- Step 10 (architectural improvement): Rich transcript object ---
        session.current_transcript = {
            "text": text,
            "language": "unknown",   # Language detection stage will update this later
            "confidence": 1.0,       # Groq translations API does not expose confidence; default to 1.0
            "timestamp": datetime.now().isoformat(),
        }

        # --- Step 6: Add to conversation history ---
        session.conversation.add_user(session.current_transcript["text"])

        # --- Step 7: Clean up temp audio file now that we have the text ---
        AudioService.cleanup_chunk(session.current_chunk)

        return session