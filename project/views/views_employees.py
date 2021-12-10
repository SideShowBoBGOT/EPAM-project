"""
Module contains all functions working on employees page.

Functions:
    employees_page()
    edit_emp(id)
    delete_emp(id)
    check_session()
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

BASE_URL = 'http://127.0.0.1:5000/'
ADMIN = User.query.get(1).login
api_employees = Blueprint('api_employees', __name__)


@api_employees.route('/employees/<string:ids>', methods=['POST', 'GET'])
@api_employees.route('/employees', defaults={'ids': None}, methods=['POST', 'GET'])
@login_required
def employees_page(ids):
    """
    Function working on employees page:
        1) adding new employees session is used by admin;
        2) Finding employees by dates of birth;
    :return: the template of the employees page
    """
    departments = Departments.query.all()
    employees = Employees.query.all()
    if ids:
        ids = list(map(lambda x: int(x), ids.split('.')))
        employees = list(filter(lambda x: x.id in ids, Employees.query.all()))
    if request.method == 'POST':
        name = str(request.form.get('name'))
        department = str(request.form.get('department'))
        salary = str(request.form.get('salary'))
        birth_date = str(request.form.get('birth_date'))
        from_date = request.form.get('From')
        to_date = request.form.get('To')
        if from_date and to_date:
            data = f'?login={session["user"][0]}&password={session["user"][1]}' \
                   f'&from_date={from_date}&to_date={to_date}&page=True'
            return redirect('/api/employees/find' + data)
        elif session.get('user') and session.get('user')[0] == ADMIN:
            data = f'?login={session["user"][0]}&password={session["user"][1]}' \
                   f'&name={urllib.parse.quote(name)}&department={urllib.parse.quote(department)}' \
                   f'&salary={urllib.parse.quote(salary)}&birth_date={birth_date}&page=True'
            return redirect('/api/employees/add' + data)
    if session.get('user') and session.get('user')[0] == ADMIN:
        return render_template('employees.html', employees=employees, departments=departments)
    return render_template('employees_for_users.html', employees=employees, departments=departments)


@api_employees.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_emp(id):
    """
    Function editing information about specific employee.
    :param id: id of the specific employee an admin wants to change information about
    :return: return template of the departments page or redirects to employees page
    """
    if session.get('user') and session.get('user')[0] == ADMIN:
        departments = Departments.query.all()
        employees = Employees.query.all()
        if Employees.query.get(id):
            if request.method == 'POST':
                name = request.form.get('new_name')
                department = request.form.get('new_department')
                salary = request.form.get('new_salary')
                birth_date = request.form.get('new_birth_date')
                data = f'?login={session["user"][0]}&password={session["user"][1]}' \
                       f'&id={id}&name={urllib.parse.quote(name)}&department={urllib.parse.quote(department)}' \
                       f'&salary={urllib.parse.quote(salary)}&birth_date={birth_date}&page=True'
                return redirect('/api/employees/edit' + data)
            return render_template('employees.html', id=id, departments=departments, employees=employees)
        return redirect('/employees')


@api_employees.route('/employees/<int:id>/del')
@login_required
def delete_emp(id):
    """
    Function deleting specific employee by its id.
    :param id: id of the specific employee an admin wants to delete
    :return: redirects to the employees page
    """
    if session.get('user') and session.get('user')[0] == ADMIN:
        data = f'?login={session["user"][0]}&password={session["user"][1]}' \
               f'&id={id}&page=True'
        return redirect('/api/employees/del' + data)


@api_employees.before_request
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
