from flask import jsonify, request


def register_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Screemer API!"})

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})