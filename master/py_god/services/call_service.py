from models.call_state import CallState
from services.session_service import call_manager
from services.audio_service import AudioService
from services.audio_queue_service import AudioQueueService


class CallService:
    @staticmethod
    def start_call(language: str = "english"):
        call = call_manager.create_call()
        if call:
            lang = language.lower().strip()
            call.preferred_language = lang if lang in ("english", "hindi") else "english"
        return call.to_dict() if call else None

    @staticmethod
    def get_call(call_id):
        return call_manager.get_call(call_id)

    @staticmethod
    def end_call(call_id):
        return call_manager.end_call(call_id)

    @staticmethod
    def receive_audio(call_id, audio_data: bytes) -> bool:
        call_session = call_manager.get_call(call_id)
        if not call_session or not call_session.active:
            return False

        # 1. Save temp file and create AudioChunk
        chunk = AudioService.save_chunk(call_session, audio_data)

        # 2. Validate AudioChunk
        if not chunk.validate():
            # Clean up invalid file
            AudioService.cleanup_chunk(chunk)
            return False

        # 3. Attach to CallSession.current_chunk
        call_session.current_chunk = chunk

        # 4. Push into CallSession.chunk_queue and mark session as ready for processing
        AudioQueueService.push(call_session, chunk)
        call_session.set_state(CallState.LISTENING)

        return True