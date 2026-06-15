import threading
import time

from models.call_state import CallState
from services.audio_service import AudioService
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

    def run_forever(self):
        """
        Background loop — polls all active sessions for queued audio chunks.

        Per-chunk flow (Steps 8 & 10):
            1. Pop chunk from queue
            2. Assign to session.current_chunk
            3. Run PipelineExecutor.execute()
               └─ STTStage   : transcribe → current_text, current_transcript,
                                conversation.add_user(), cleanup temp file
               └─ MemoryStage  : (placeholder)
               └─ ContextStage : (placeholder)
               └─ AIStage      : (placeholder)
               └─ TTSStage     : (placeholder)
            4. mark_processed()
            5. Ensure temp file is cleaned up (double-safety if STT failed mid-way)
            6. session.current_chunk = None
            7. state → IDLE
        """
        while self.running:
            try:
                calls = list(call_manager.calls.values())
                for session in calls:
                    # Only pick up sessions ready for processing
                    if not session.is_listening():
                        continue
                    if not session.active:
                        continue
                    if getattr(session, 'processing', False):
                        continue
                    if AudioQueueService.is_empty(session):
                        continue

                    chunk = AudioQueueService.pop(session)
                    if chunk is None:
                        continue

                    session.current_chunk = chunk
                    session.processing = True

                    try:
                        # Steps 8 & 9: run the full pipeline
                        # STTStage internally handles TRANSCRIBING state + cleanup.
                        # Worker sets THINKING / SPEAKING at the right moments.
                        session.set_state(CallState.TRANSCRIBING)
                        self.pipeline.execute(session)

                        # Pipeline completed successfully
                        chunk.mark_processed()

                    except Exception as e:
                        print(f"[Worker] Error processing chunk {chunk.chunk_id} "
                              f"for call {session.call_id}: {e}")
                        # Return to LISTENING so the session can still accept the next chunk
                        session.set_state(CallState.LISTENING)

                    finally:
                        # Step 8: clean up temp file regardless of success/failure
                        # (STTStage already does this on success; this is a safety net)
                        AudioService.cleanup_chunk(chunk)

                        # Step 8: clear current_chunk pointer
                        session.current_chunk = None

                        session.processing = False

                        # Step 8: advance to IDLE only if we didn't roll back to LISTENING
                        if session.state not in (CallState.LISTENING, CallState.ENDED):
                            session.set_state(CallState.IDLE)

            except Exception as e:
                print(f"[Worker] Unexpected error in main loop: {e}")

            time.sleep(0.1)  # Prevent busy-wait / high CPU usage