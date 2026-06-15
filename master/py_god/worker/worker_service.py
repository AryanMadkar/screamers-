import threading
import time
from services.session_service import call_manager
from services.audio_queue_service import AudioQueueService

class WorkerService:
    def __init__(self):
        self.running = False
        self.thread = None
        
    def start(self):
        try:
            if self.running:
                print("Worker is already running.")
                return
            
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            print("Worker started.")
        except Exception as e:
            print(f"Error starting worker: {e}")
            return
    def stop(self):
        try:
            if not self.running:
                print("Worker is not running.")
                return

            self.running = False
            if self.thread:
                self.thread.join()
            print("Worker stopped.")
        except Exception as e:
            print(f"Error stopping worker: {e}")
            return
    def run_forever(self):
        try:
            while self.running:
                calls = list(call_manager.calls.values())
                for session in calls:
                    if not session.active:
                        continue
                    if session.processing:
                        continue
                    if AudioQueueService.is_empty(session):
                        continue
                    session.processing = True
                    chunk = AudioQueueService.pop(session)
                    if chunk is None:
                        session.processing = False
                        continue
                    session.current_chunk = chunk
                    #
                    # Future STT goes here
                    #

                    #
                    # Future LangGraph goes here
                    #
                    chunk.mark_processed()
                    session.processing = False
                    time.sleep(0.1)  # Sleep briefly to prevent tight loop
        except Exception as e:
            print(f"Error in worker loop: {e}")
            return