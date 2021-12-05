"""
Module contains functions to work with User DB( CRUD operations ).

Functions:
    add_user(login, password)
    change_user(id, login, password)
    del_user(id)
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from f_logger import logger
from application import db
from models.users import User


def add_user(login, password):
    """
    Function adding new user
    :param login: new login
    :param password: new password
    :return: None
    """
    try:
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
    except:
        logger.warning('DB can`t add user')
    return None


def change_user(id, login, password):
    """
    Function changing users information
    :param id: id of the user an admin wants to change
    :return: None
    """
    try:
        user = User.query.get(id)
        user.login = login
        user.password = password
        db.session.commit()
    except:
        logger.warning('DB can`t change user`s data')
    return None


def del_user(id):
    """
    Function deleting user from db
    :param id: if of the user
    :return: None
    """
    user = User.query.get(id)
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        logger.warning('DB can`t delete user')
    return None
