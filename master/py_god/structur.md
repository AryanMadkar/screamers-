voice_ai/
│
├── app.py
├── config.py
├── requirements.txt
│
├── api/
│   └── routes.py
│
├── models/
│   ├── call_session.py
│   ├── conversation.py
│   ├── message.py
│   └── audio_chunk.py
│
├── managers/
│   └── call_manager.py
│
├── services/
│   ├── call_service.py
│   ├── session_service.py
│   ├── audio_service.py
│   ├── audio_queue_service.py
│   └── stt_service.py
│
├── worker/
│   └── worker_service.py
│
├── pipeline/
│   ├── pipeline_executor.py
│   └── stages/
│       ├── ai_stage.py
│       ├── context_stage.py
│       ├── memory_stage.py
│       ├── stt_stage.py
│       └── tts_stage.py
│
├── graph/
│   ├── graph_builder.py
│   └── nodes.py
│
├── database/
│   └── __init__.py
│
└── temp/