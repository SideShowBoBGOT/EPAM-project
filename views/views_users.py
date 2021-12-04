import os
import sys
from flask import current_app, abort
from flask_login import login_user, login_required, logout_user
import logging


sys.path.append(os.path.abspath(os.path.join('..')))

from models.users import User
from service import add_user, del_user, change_user
from flask import render_template, request, redirect, Blueprint, url_for, session
from .views_login import api_login
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
            return redirect('/users')
        return render_template('users_for_admin.html', users=users)
    elif User.query.filter_by(login=session.get('user')).all():
        user = User.query.filter_by(login=session.get('user')).first()
        return render_template('users.html', user=user)
    abort(401)

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
                    change_user(id, login, password)
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
            del_user(id)
        return redirect('/users')

@api_users.before_request
def check_session():
    users = User.query.filter_by(login=session.get('user')).all()
    if users:
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')


