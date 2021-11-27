from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    db.init_app(app)
    # from models.employees import Employees
    # from models.departments import Departments
    # from models.users import User
    login_manager.init_app(app)
    login_manager.login_view = "api.login_page"
    # db.create_all()
    from views.api import api
    app.register_blueprint(api)
    from rest.rest_api import r_api
    r_api.init_app(app)

    return app

