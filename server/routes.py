from flask import jsonify, request
from llm import generate_response

def register_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Screemer API!"})

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})
    
    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        response = generate_response(user_message)
        return jsonify({"response": response})