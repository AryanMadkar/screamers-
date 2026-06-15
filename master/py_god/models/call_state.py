from enum import Enum


class CallState(Enum):

    IDLE = "idle"

    LISTENING = "listening"

    TRANSCRIBING = "transcribing"

    THINKING = "thinking"

    SPEAKING = "speaking"

    ENDED = "ended"