from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

from routes.task_routes import task_bp
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(debug=True)
