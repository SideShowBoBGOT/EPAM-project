from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config
import logging


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
    from views import api
    from views import api_users
    from views import api_login
    from views import api_employees
    from views import api_departments
    app.register_blueprint(api)
    app.register_blueprint(api_departments)
    app.register_blueprint(api_employees)
    app.register_blueprint(api_login)
    app.register_blueprint(api_users)
    from rest import r_api
    r_api.init_app(app)
    return app
