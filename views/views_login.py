"""
Module contains all functions working on login page.

Functions:
    login_page()
    logout_page()
    make_session_permanent()
    redirect_to_sign_in(response)
"""
import os
import sys
from flask_login import login_user, login_required, logout_user
from flask import render_template, request, redirect, Blueprint, url_for, session

sys.path.append(os.path.abspath(os.path.join('..')))

from models.users import User
from f_logger import logger
api_login = Blueprint('api_login', __name__)


@api_login.route('/', methods=['GET', 'POST'])
def login_page():
    """
    Function returning the template of the main page
    :return: the template of the main page
    """
    logout_user()
    session.clear()
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.password == password:
                login_user(user)
                session['user'] = login
                logger.info(f'Authorized: login: "{login}"\tpassword: "{password}"')
                return redirect('/departments')
        else:
            logger.info(f'Failed authorization: login: "{login}"\tpassword: "{password}"')
    return render_template('index.html')


@api_login.route('/logout')
@login_required
def logout_page():
    """
    Function logging user out
    :return: redirect  to the main page
    """
    logout_user()
    logger.info('User logged out')
    return redirect('/')


@api_login.before_request
def make_session_permanent():
    """
    Function making sessions permanent
    :return: None
    """
    session.permanent = False


@api_login.after_request
def redirect_to_sign_in(response):
    """
    Function redirecting user to the main page if not logged in.
    Else redirects to the next page.
    :param response: the next page user wants to visit
    :return: redirect to the main page or response
    """
    if response.status_code == 401:
        return redirect('/')
    return response
