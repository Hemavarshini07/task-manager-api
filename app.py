from flask import Flask
import config
from models import db

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

from routes.task_routes import task_bp
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
