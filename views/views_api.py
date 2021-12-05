"""
Module contains all functions working on api page.

Functions:
    api_page()
    check_session()
"""
import os
import sys
from flask import render_template, redirect, Blueprint, session
from flask_login import login_user, login_required


sys.path.append(os.path.abspath(os.path.join('..')))
from models.users import User
ADMIN = User.query.get(1).login

api = Blueprint('api', __name__)

@api.route('/api_list')
@login_required
def api_page():
    """
    Function returning API page
    :return: template of API page
    """
    return render_template('API.html')

@api.before_request
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