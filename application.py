"""
Module containing factory for app merging it with database, blueprints, REST.

Functions:
    create_app()
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """
    Function creating app and merging it with db, blueprints
    and REST.
    :return: application instance
    """
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
    from views import api_users
    from views import api_login
    from views import api_employees
    from views import api_departments
    app.register_blueprint(api_departments)
    app.register_blueprint(api_employees)
    app.register_blueprint(api_login)
    app.register_blueprint(api_users)
    from rest import r_api
    r_api.init_app(app)
    return app
