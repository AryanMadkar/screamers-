from flask import Flask
from api.routes import router
from worker.worker_service import WorkerService

app = Flask(__name__)
app.register_blueprint(router)
worker_service = WorkerService()
worker_service.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)