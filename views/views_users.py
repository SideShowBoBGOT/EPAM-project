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
import requests
from flask_login import login_user, login_required
from flask import render_template, request, redirect, Blueprint, session

sys.path.append(os.path.abspath(os.path.join('..')))

from models.users import User

ADMIN = User.query.get(1).login
BASE_URL = 'http://127.0.0.1:5000/'
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
    if session.get('user') and session.get('user')[0] == ADMIN:
        users = User.query.all()
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            data = {'login': session['user'][0], 'password': session['user'][1],
                    'new_login': login, 'new_password': password}
            requests.post(BASE_URL + 'api/users/add', data=data)
            return redirect('/users')
        return render_template('users_for_admin.html', users=users)
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
    if session.get('user') and session.get('user')[0] == ADMIN:
        users = User.query.all()
        if User.query.get(id):
            if request.method == 'POST':
                login = request.form.get('new_login')
                password = request.form.get('new_password')
                data = {'login': session['user'][0], 'password': session['user'][1],
                        'id': id, 'new_login': login, 'new_password': password}
                requests.post(BASE_URL + 'api/users/edit', data=data)
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
    if session.get('user') and session.get('user')[0] == ADMIN:
        data = {'login': session['user'][0], 'password': session['user'][1], 'id': id}
        requests.post(BASE_URL + 'api/users/del', data=data)
        return redirect('/users')


@api_users.before_request
def check_session():
    """
    Function logging in user to the page if session has been
    already created. Else redirects to the main page.
    :return: None or redirect
    """
    if session.get('user') and session.get('user')[0] == ADMIN:
        users = User.query.filter_by(login=session.get('user')[0]).all()
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')
