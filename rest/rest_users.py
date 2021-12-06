"""
Module contains classes to work with REST API for User.

Classes:
    UserAPIget(Resource)
    UserAPIadd(Resource)
    UserAPIedit(Resource)
    UserAPIdel(Resource)
"""
import os
import sys
from flask import redirect
from flask_restful import Resource, abort, reqparse

sys.path.append(os.path.abspath(os.path.join('..')))

from .common_funcs import check_empty_strings
from models.users import User
from service import add_user, del_user, change_user
from f_logger import logger

get_args = reqparse.RequestParser()
get_args.add_argument("login", type=str, help="User`s login", required=True)
get_args.add_argument("password", type=str, help="User`s password", required=True)

add_args = reqparse.RequestParser()
add_args.add_argument("login", type=str, help="User`s login", required=True)
add_args.add_argument("password", type=str, help="User`s password", required=True)
add_args.add_argument("new_login", type=str, help="Login of new user", required=True)
add_args.add_argument("new_password", type=str, help="Password of new user", required=True)
add_args.add_argument("page", type=str, help="Redirects to prev page")

edit_args = reqparse.RequestParser()
edit_args.add_argument("login", type=str, help="User`s login", required=True)
edit_args.add_argument("password", type=str, help="User`s password", required=True)
edit_args.add_argument("new_login", type=str, help="New user`s login", required=True)
edit_args.add_argument("new_password", type=str, help="New user`s password", required=True)
edit_args.add_argument("id", type=int, help="Id of the user to edit", required=True)
edit_args.add_argument("page", type=str, help="Redirects to prev page")

del_args = reqparse.RequestParser()
del_args.add_argument("login", type=str, help="User`s login", required=True)
del_args.add_argument("password", type=str, help="User`s password", required=True)
del_args.add_argument("id", type=int, help="Id of the user to delete", required=True)
del_args.add_argument("page", type=str, help="Redirects to prev page")


class UserAPIget(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for giving info about users of the table.

    Methods:
        get(self)
    """
    def get(self):
        """
        Method overrides get method of Resource and
        works on get method, giving info about users,
        only if credentials are correct.
        :return: dict of user information
        """
        args = get_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password:
            # admin`s id is 1
            if user.id == 1 and user.password == password:
                users = dict()
                for usr in User.query.all():
                    users[usr.id] = {'id': usr.id, 'login': usr.login,
                                     'password': usr.password}
                return users
            return {'id': user.id, 'login': user.login,
                    'password': user.password}
        abort(401, error='CREDENTIALS_INCORRECT')


class UserAPIadd(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for adding users to the table.

    Methods:
        get(self)
    """
    def get(self):
        """
         Method overrides get method of Resource and
         works on get method, adding users,
         only if arguments and credentials are correct.
         :return: dict of messages or errors
        """
        args = add_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        new_login = args['new_login']
        new_password = args['new_password']
        page = args.get('page')
        if user and user.id == 1 and user.password == password:
            if check_empty_strings(new_login, new_password):
                if not User.query.filter_by(login=new_login).first():
                    add_user(new_login, new_password)
                    logger.info(f'Added user: new_login: "{new_login}"\tnew_password: "{new_password}"')
                    if page and page == 'True':
                        return redirect('/users')
                    return {'message': 'ADD_SUCCESS'}
            logger.info(f'Failed adding user: new_login: "{new_login}"\tnew_password: "{new_password}"')
            if page and page == 'True':
                return redirect('/users')
            abort(401, error='VALUES_INCORRECT')
        logger.info(f'Failed adding user: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class UserAPIedit(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for editing users of the table.

    Methods:
        get(self)
    """
    def get(self):
        """
         Method overrides get method of Resource and
         works on get method, editing users,
         only if arguments and credentials are correct.
         :return: dict of messages or errors
        """
        args = edit_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        new_login = args['new_login']
        new_password = args['new_password']
        id = args['id']
        page = args.get('page')
        if user and user.id == 1 and user.password == password:
            if check_empty_strings(new_login, new_password) and User.query.get(id) \
                    and (not User.query.filter_by(login=new_login).first() or User.query.get(id).login == new_login):
                change_user(id, new_login, new_password)
                logger.info(f'Edited user: id: "{id}" new_login: "{new_login}"\tnew_password: "{new_password}"')
                if page and page == 'True':
                    return redirect('/users')
                return {'message': 'EDIT_SUCCESS'}
            logger.info(f'Edited user: id: "{id}" new_login: "{new_login}"\tnew_password: "{new_password}"')
            if page and page == 'True':
                return redirect('/users')
            abort(401, error='VALUES_INCORRECT')
        logger.info(f'Failed editing user: "{login}"\tpassword: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class UserAPIdel(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for deleting users from the table.

    Methods:
        get(self)
    """
    def get(self):
        """
         Method overrides get method of Resource and
         works on get method, deleting users,
         only if arguments and credentials are correct.
         :return: dict of messages or errors
        """
        args = del_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        id = args['id']
        page = args.get('page')
        # admin`s id is 1
        if user and user.id == 1 and user.password == password:
            if User.query.get(id):
                if id != 1:
                    del_user(id)
                    logger.info(f'Deleted user: id: "{id}"')
                    if page and page == 'True':
                        return redirect('/users')
                    return {'message': 'DEL_SUCCESS'}
            logger.info(f'Failed deleting user: id: "{id}"')
            if page and page == 'True':
                return redirect('/users')
            abort(401, error='VALUES_INCORRECT')
        logger.info(f'Failed deleting user: "{login}"\tpassword: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')
