class AudioQueueService:

    @staticmethod
    def push(call_session, chunk):
        call_session.chunk_queue.append(chunk)

    @staticmethod
    def pop(call_session):

        if len(call_session.chunk_queue) == 0:
            return None

        return call_session.chunk_queue.pop(0)

    @staticmethod
    def size(call_session):
        return len(call_session.chunk_queue)
    
    @staticmethod
    def is_empty(call_session):
        return len(call_session.chunk_queue) == 0