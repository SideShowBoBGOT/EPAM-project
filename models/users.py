"""
Module contains class User for DB.

Classes:
    User(db.Model, UserMixin)
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from application import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Class is descendant of db.Model and UserMixin.
    It creates table User in db.
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
