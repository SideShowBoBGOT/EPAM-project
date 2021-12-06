"""
Module contains all functions working on departments page.

Functions:
    departments_page()
    delete_dnt(id)
    edit_dnt(id)
"""
import os
import sys
import urllib.parse
from flask_login import login_user, login_required

sys.path.append(os.path.abspath(os.path.join('..')))

from models.employees import Employees
from models.departments import Departments
from models.users import User
from flask import render_template, request, redirect, Blueprint, session
from migrations.migrations_funcs import avg_salaries

ADMIN = User.query.get(1).login
BASE_URL = 'http://127.0.0.1:5000/'
api_departments = Blueprint('api_departments', __name__)


@api_departments.route('/departments', methods=['POST', 'GET'])
@login_required
def departments_page():
    """
    Function working on departments page:
        1) adding new departments if method "POST" received session is used by admin
        2) showing the table of the departments
    :return: the template of the departments page
    """
    departments = Departments.query.all()
    employees = Employees.query.all()
    dnt_salary = avg_salaries(departments, employees)
    department = request.form.get('department')
    if session.get('user') and session.get('user')[0] == ADMIN:
        if request.method == 'POST':
            data =f'?login={session["user"][0]}' \
                   f'&password={session["user"][1]}&department={urllib.parse.quote(department)}&page=True'
            return redirect('/api/departments/add' + data)
        return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)
    return render_template('departments_for_users.html', departments=departments, dnt_salary=dnt_salary)


@api_departments.route('/departments/<int:id>/del')
@login_required
def delete_dnt(id):
    """
    Function deleting specific department by its id
    :param id: id of the specific department an admin wants to delete
    :return: redirects user to the departments page
    """
    if session.get('user') and session.get('user')[0] == ADMIN:
        data = f'?login={session["user"][0]}&password={session["user"][1]}&id={id}&page=True'
        return redirect('/api/departments/del' + data)


@api_departments.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_dnt(id):
    """
    Function editing information about specific departments
    :param id:  id of the specific department
    :return: the template of the employees page or redirects to departments
    """
    if session.get('user') and session.get('user')[0] == ADMIN:
        departments = Departments.query.all()
        employees = Employees.query.all()
        dnt_salary = avg_salaries(departments, employees)
        department = request.form.get('new_department')
        if Departments.query.get(id):
            if request.method == 'POST':
                data = f'?login={session["user"][0]}&password={session["user"][1]}' \
                       f'&id={id}&department={urllib.parse.quote(department)}&page=True'
                return redirect('/api/departments/edit' + data)
            return render_template('departments.html', id=id, departments=departments, dnt_salary=dnt_salary)
        return redirect('/departments')


@api_departments.before_request
def check_session():
    """
      Function logging in user to the page if session has been
      already created. Else redirects to the main page.
      :return: None or redirect
    """
    if session.get('user'):
        users = User.query.filter_by(login=session.get('user')[0]).all()
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')
