from dotenv import load_dotenv
import os
load_dotenv()


class Config:
    PORT = os.getenv('PORT', 8000)
    Debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    MODEL_PATH = os.getenv("MODEL_PATH")
    N_CTX = int(os.getenv("N_CTX", 4096))
    N_THREADS = int(os.getenv("N_THREADS", 8))
    N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", -1))
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")