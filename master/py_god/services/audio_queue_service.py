from models.call_session import CallSession
from models.audio_chunk import AudioChunk

class AudioQueueService:
    @staticmethod
    def push(session: CallSession, chunk: AudioChunk) -> bool:
        try:
            session.chunk_queue.append(chunk)
            return True
        except Exception as e:
            print(f"Error pushing chunk to queue: {e}")
            return False

    @staticmethod
    def pop(session: CallSession) -> AudioChunk:
        try:
            if session.chunk_queue:
                return session.chunk_queue.pop(0)
            return None
        except Exception as e:
            print(f"Error popping chunk from queue: {e}")
            return None

    @staticmethod
    def is_empty(session: CallSession) -> bool:
        try:
            return len(session.chunk_queue) == 0
        except Exception as e:
            print(f"Error checking if queue is empty: {e}")
            return True