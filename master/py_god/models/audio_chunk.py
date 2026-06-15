import uuid
import os

class AudioChunk:
    def __init__(self, data: bytes, format: str = "wav"):
        self.chunk_id = str(uuid.uuid4())
        self.data = data
        self.format = format
        self.file_path = None
        self.processed = False

    def validate(self) -> bool:
        if not self.file_path:
            return False
        if not os.path.exists(self.file_path):
            return False
        if os.path.getsize(self.file_path) == 0:
            return False
        return True
    
    def mark_processed(self):
        self.processed = True