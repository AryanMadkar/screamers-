import sys
import io
# Force UTF-8 output so Hindi/emoji strings never crash on Windows cp1252 terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask
from api.routes import router
from worker.worker_service import WorkerService

app = Flask(__name__)
app.register_blueprint(router)

# Initialize and start the background worker service
worker = WorkerService()
worker.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)