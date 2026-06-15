import os
from config import Config
from models.audio_chunk import AudioChunk

class AudioService:
    @staticmethod
    def save_chunk(call_session, audio_data: bytes) -> AudioChunk:
        try:
            # Ensure the temp folder exists
            os.makedirs(Config.TEMP_FOLDER, exist_ok=True)
            
            # Create AudioChunk
            chunk = AudioChunk(data=audio_data)
            
            # Save chunk data to temporary file
            filename = f"chunk_{call_session.call_id}_{chunk.chunk_id}.wav"
            file_path = os.path.join(Config.TEMP_FOLDER, filename)
            
            with open(file_path, "wb") as f:
                f.write(audio_data)
                
            chunk.file_path = file_path
            
            # Update session
            call_session.current_chunk = chunk
            return chunk
        except Exception as e:
            raise Exception(f"Error saving audio chunk: {e}")

    @staticmethod
    def cleanup_chunk(chunk: AudioChunk):
        try:
            if chunk and chunk.file_path and os.path.exists(chunk.file_path):
                os.remove(chunk.file_path)
        except Exception as e:
            print(f"Error cleaning up audio chunk file: {e}")