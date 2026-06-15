from typing import TypedDict


class VoiceState(TypedDict):
    conversation_id: str
    messages: list[dict]
    audio_path: str
    language: str
    current_text: str
    text: str