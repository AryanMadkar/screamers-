import threading
import time

from models.call_state import CallState
from services.session_service import call_manager
from services.audio_queue_service import AudioQueueService
from pipeline.pipeline_executor import PipelineExecutor

class WorkerService:
    def __init__(self):
        self.running = False
        self.thread = None
        self.pipeline = PipelineExecutor()
        
    def start(self):
        try:
            if self.running:
                print("Worker is already running.")
                return
            
            self.running = True
            self.thread = threading.Thread(target=self.run_forever, daemon=True)
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
        while self.running:
            try:
                calls = list(call_manager.calls.values())
                for session in calls:
                    if not session.is_listening():
                        continue
                    if not session.active:
                        continue
                    if getattr(session, 'processing', False):
                        continue
                    if AudioQueueService.is_empty(session):
                        continue

                    session.processing = True
                    chunk = AudioQueueService.pop(session)
                    if chunk is None:
                        session.processing = False
                        continue

                    session.current_chunk = chunk

                    try:
                        # Phase 1: Transcribe audio -> text
                        session.set_state(CallState.TRANSCRIBING)
                        self.pipeline.stt.process(session)

                        # Phase 2: Build memory + context, then call AI
                        session.set_state(CallState.THINKING)
                        self.pipeline.memory.process(session)
                        self.pipeline.context.process(session)
                        self.pipeline.ai.process(session)

                        # Phase 3: Synthesize AI response to audio
                        session.set_state(CallState.SPEAKING)
                        self.pipeline.tts.process(session)

                        chunk.mark_processed()

                    except Exception as e:
                        print(f"Error processing chunk for call {session.call_id}: {e}")
                        # On error, return to LISTENING so the next chunk can still be processed
                        session.set_state(CallState.LISTENING)
                    finally:
                        session.processing = False
                        # Only reset to IDLE if we finished successfully (not already overridden)
                        if session.state != CallState.LISTENING:
                            session.set_state(CallState.IDLE)

            except Exception as e:
                print(f"Error in worker loop: {e}")

            time.sleep(0.1)  # Sleep briefly to prevent high CPU usage in empty loop