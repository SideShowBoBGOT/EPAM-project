from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from project.api import api
    app.register_blueprint(api)

    return app

