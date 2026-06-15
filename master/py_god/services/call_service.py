from services.session_service import call_manager
from services.audio_service import AudioService
from graph.graph_builder import graph

class CallService:
    @staticmethod
    def start_call():
        call = call_manager.create_call()
        return call.to_dict() if call else None

    @staticmethod
    def get_call(call_id):
        return call_manager.get_call(call_id)

    @staticmethod
    def end_call(call_id):
        return call_manager.end_call(call_id)

    @staticmethod
    def process_audio(call_id, audio_data: bytes):
        call_session = call_manager.get_call(call_id)
        if not call_session:
            return None
            
        # 1. Save audio chunk and update session's current_chunk
        AudioService.save_chunk(call_session, audio_data)
        
        # 2. Invoke Graph Pipeline passing call_session
        graph.invoke(call_session)
        
        # 3. Clean up temporary audio file after processing
        AudioService.cleanup_chunk(call_session.current_chunk)
        
        return call_session

    @staticmethod
    def receive_audio(call_id, audio_data: bytes) -> bool:
        call_session = call_manager.get_call(call_id)
        if not call_session:
            return False
            
        # 1. Save temp file and Create AudioChunk
        chunk = AudioService.save_chunk(call_session, audio_data)
        
        # 2. Validate AudioChunk
        if not chunk.validate():
            # Clean up invalid file
            AudioService.cleanup_chunk(chunk)
            return False
            
        # 3. Attach to CallSession.current_chunk (Done in save_chunk, but explicit here for clarity)
        call_session.current_chunk = chunk
        
        # 4. Push into CallSession.chunk_queue
        call_session.chunk_queue.append(chunk)
        
        return True