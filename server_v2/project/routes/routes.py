from flask import jsonify, request
from services.chat_service import chat  # FIX: was using generate_response directly, bypassing all service logic


def register_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Screemer API!"})

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.route("/chat", methods=["POST"])
    def chat_route():
        data = request.get_json()

        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # FIX: original endpoint ignored user_id and conversation_id entirely
        user_id = data.get("user_id")          # optional — None triggers new user creation
        conversation_id = data.get("conversation_id")  # optional — None triggers new conversation

        result = chat(user_id, conversation_id, user_message)
        return jsonify(result)
