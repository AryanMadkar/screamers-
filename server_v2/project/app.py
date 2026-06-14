from dotenv import load_dotenv
load_dotenv()  # FIX: Must be called BEFORE importing Config or any module that reads env vars

from flask import Flask
from config import Config
from routes.routes import register_routes
from services.llm import get_llm
from database.db import create_indexes

create_indexes()

app = Flask(__name__)
app.config.from_object(Config)
register_routes(app)

print("Preloading model...")
get_llm()
print("Model preloaded!")

print(f"Starting server on port {Config.PORT} with debug={Config.Debug}")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.Debug)
