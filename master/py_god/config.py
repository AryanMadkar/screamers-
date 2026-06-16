import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    """
    Central configuration for the application.
    """

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found in environment variables."
        )
        
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("PORT", 5000))

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "whisper-large-v3"
    )

    # Alias used by GroqSTT — same value, kept separate so renaming one doesn't break the other
    GROQ_MODEL = MODEL_NAME

    TEMP_FOLDER = os.getenv(
        "TEMP_FOLDER",
        "./temp"
    )

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/screem"
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "screem"
    )

    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "llama-3.3-70b-versatile"
    )