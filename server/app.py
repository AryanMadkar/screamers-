from dotenv import load_dotenv
from flask import Flask
from config import Config
from routes import register_routes
from llm import get_llm
import os

HF_TOKEN = os.getenv("HF_TOKEN")

app = Flask(__name__)
app.config.from_object(Config)
register_routes(app)
print("preloading model...")
get_llm()
print("Model preloaded!")

print(f"Starting server on port {Config.PORT} with debug={Config.Debug}")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.Debug)