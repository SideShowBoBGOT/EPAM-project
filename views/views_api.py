import os
import sys
from flask import render_template, redirect, Blueprint, session
from flask_login import login_user, login_required
import logging

from flask import current_app


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
    users = User.query.filter_by(login=session.get('user')).all()
    if users:
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')