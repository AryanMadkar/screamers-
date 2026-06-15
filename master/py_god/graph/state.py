from typing import TypedDict


class VoiceState(TypedDict):

    conversation_id: str

    audio_path: str

    text: str