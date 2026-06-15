from flask import Flask, request, jsonify
from config import Config
from graph.graph_builder import graph
from services.conversation_manager import ConversationManager
import tempfile
import os
app = Flask(__name__)


@app.route("/conversation/start", methods=["POST"])
def start():
    try:
          
        audio = request.files.get("audio_path")

        if audio is None:
            return jsonify({"error": "Missing audio"}), 400

        # Save temporarily
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        
        temp.close()  # Close the file so that it can be written to on Windows
        audio.save(temp.name)
        print(temp.name)

        conversation_id = ConversationManager.create_conversation()

        state = {
            "conversation_id": conversation_id,
            "messages": [],
            "language": "unknown",
            "audio_path": temp.name,
            "current_text": "",
            "text": ""
        }

        result = graph.invoke(state)

        os.remove(temp.name)

        return jsonify({
            "conversation_id": conversation_id,
            "message": result["messages"],
            "language": result["language"]
        })
    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host=Config.FLASK_HOST, port=Config.FLASK_PORT)