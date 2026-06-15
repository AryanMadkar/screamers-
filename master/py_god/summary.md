# Voice AI - Refactoring & Queue Integration Summary

This document summarizes the refactoring and structural changes implemented to finalize **Phase 2** and prepare for **Phase 3**.

---

## 1. Directory Structure
The workspace has been organized as follows:

```
voice_ai/
│
├── app.py                      # Tiny Flask app initialization and worker thread starter
├── config.py                   # App configurations (Groq API, folders, host/port)
├── requirements.txt            # Dependency listings
├── structur.md                 # Updated structural map of the project
│
├── api/
│   └── routes.py               # REST API endpoints (start, end, status, and audio ingest)
│
├── models/
│   ├── call_session.py         # In-memory call session states (tracks queue, language, context, etc.)
│   ├── conversation.py         # Manages conversation history (user and assistant messages)
│   ├── message.py              # Message model tracking role, content, and timestamp
│   └── audio_chunk.py          # Tracks audio segments, temporary paths, and verification status
│
├── managers/
│   └── call_manager.py         # Controls active sessions (creation, retrieval, removal)
│
├── services/
│   ├── call_service.py         # Entry point for session flows and routing ingest logic
│   ├── session_service.py      # Standard manager instantiator
│   ├── audio_service.py        # Manages writing/reading segments to Config.TEMP_FOLDER
│   ├── audio_queue_service.py  # Encapsulates queue operations (push, pop, empty checks)
│   └── stt_service.py          # Audio transcription via Groq API
│
├── worker/
│   └── worker_service.py       # Background thread consumer that processes audio chunks sequentially
│
├── pipeline/
│   ├── pipeline_executor.py    # Defines stages execution sequence
│   └── stages/                 # Pipeline stages (STT, Memory, Context, AI, TTS)
│
├── graph/
│   ├── graph_builder.py        # Defines StateGraph structure (using CallSession)
│   └── nodes.py                # Graph nodes logic (speech-to-text, language detection)
│
└── database/                   # Database package folder
```

---

## 2. Worker & Pipeline Integration Changes (Bugs Fixed)
During review, several critical bugs were identified and fixed in the worker and pipeline components:

1. **Missing queue service**:
   * **Issue**: The worker imported `AudioQueueService` from `services.audio_queue_service`, but the file did not exist in the codebase.
   * **Fix**: Implemented `services/audio_queue_service.py` to correctly encapsulate queue actions (push, pop, checks) on the `CallSession.chunk_queue`.
2. **Infinite CPU / Tight Loop Bug**:
   * **Issue**: The `time.sleep(0.1)` call in `worker_service.py` was mistakenly placed inside the `finally` block instead of the `while self.running` loop, leading to 100% CPU usage.
   * **Fix**: Moved `time.sleep(0.1)` to the end of the `while` loop block.
3. **Session Processing Lock**:
   * **Issue**: The `session.processing` flag was set to `True` when consuming a chunk, but was never reset to `False` inside the loop. This locked the session permanently, preventing it from consuming any subsequent chunks.
   * **Fix**: Added `session.processing = False` at the end of the chunk consumption process in the loop.
4. **Variable Scope NameError**:
   * **Issue**: The `finally` block in the worker attempted to access `session.processing = False`, which would crash with a `NameError` if the thread exited before/outside the loop iterations.
   * **Fix**: Safely managed processing resets inside the loop and removed the unsafe `finally` block statement.
5. **Autostart Worker**:
   * **Issue**: The Flask app did not start the background thread, so chunks in the queue were never consumed.
   * **Fix**: Added initialization and `.start()` calls for the `WorkerService` directly in `app.py`.
6. **Missing properties**:
   * **Issue**: `CallSession` lacked the `processing` attribute, and `AudioChunk` lacked the `mark_processed()` method and `processed` flag.
   * **Fix**: Added these attributes/methods to the respective model classes to guarantee compatibility.
