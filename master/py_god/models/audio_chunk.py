import uuid

class AudioChunk:
    def __init__(self, data: bytes, format: str = "wav"):
        self.chunk_id = str(uuid.uuid4())
        self.data = data
        self.format = format
        self.file_path = None