"""
Module contains all functions working on users page.

Functions:
    users_page()
    edit_user(id)
    delete_user(id)
    check_session()
"""
import os
import sys
from flask_login import login_user, login_required
from flask import render_template, request, redirect, Blueprint, session

sys.path.append(os.path.abspath(os.path.join('..')))

from models.users import User
from service import add_user, del_user, change_user
from f_logger import logger
ADMIN = User.query.get(1).login
api_users = Blueprint('api_users', __name__)

@api_users.route('/users', methods=['POST', 'GET'])
@login_required
def users_page():
    """
    Function working on departments page:
        1) adding new users if method "POST" received and session is used by admin
        2) showing the table of the users
    :return: the template of the departments page
    """
    if session.get('user') == ADMIN:
        users = User.query.all()
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            if login and password and not User.query.filter_by(login=login).first():
                add_user(login, password)
                logger.info(f'Added user: login: "{login}"\tpassword: "{password}"')
            else:
                logger.info(f'Failed adding user: login: "{login}"\tpassword: "{password}"')
            return redirect('/users')
        return render_template('users_for_admin.html', users=users)
    elif User.query.filter_by(login=session.get('user')).all():
        user = User.query.filter_by(login=session.get('user')).first()
        return render_template('users.html', user=user)

@api_users.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Function editing information about specific users
    :param id: id of the specific user an admin wants to change information about
    :return: return template of the users page or redirects to users page
    """
    if session.get('user') == ADMIN:
        users = User.query.all()
        if User.query.get(id):
            if request.method == 'POST':
                login = request.form.get('new_login')
                password = request.form.get('new_password')
                if login and password and \
                        (not User.query.filter_by(login=login).first() or User.query.get(id).login == login):
                    logger.info(f'Edited user: id: "{id}" login: "{login}"\tpassword: "{password}"')
                    change_user(id, login, password)
                else:
                    logger.info(f'Failed editing user: id: "{id}" login: "{login}"\tpassword: "{password}"')
                return redirect('/users')
            return render_template('users_for_admin.html', id=id, users=users)
        return redirect('/users')

@api_users.route('/users/<int:id>/del')
@login_required
def delete_user(id):
    """
    Function deleting specific user by its id
    :param id: id of the specific user an admin wants to delete
    :return: redirects user to the users page
    """
    if session.get('user') == ADMIN:
        if User.query.get(id).login != ADMIN:
            logger.info(f'Deleted user: id: "{id}"')
            del_user(id)
        else:
            logger.info(f'Failed deleting user: id: "{id}"')
        return redirect('/users')

@api_users.before_request
def check_session():
    """
    Function logging in user to the page if session has been
    already created. Else redirects to the main page.
    :return: None or redirect
    """
    users = User.query.filter_by(login=session.get('user')).all()
    if users:
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')


