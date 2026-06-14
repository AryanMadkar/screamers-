from dotenv import load_dotenv
import os
load_dotenv()


class Config:
    PORT = os.getenv('PORT', 8000)
    Debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')