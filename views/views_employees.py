import os
import sys
import datetime
from flask_login import login_user, login_required, logout_user
import logging

from flask import current_app


sys.path.append(os.path.abspath(os.path.join('..')))

from models.employees import Employees
from models.departments import Departments
from models.users import User
from flask import Flask, render_template, request, redirect, Blueprint, url_for, session
from service import add_emp, find_emp, change_emp, del_emp

ADMIN = User.query.get(1).login
api_employees = Blueprint('api_employees', __name__)

@api_employees.route('/employees', methods=['POST', 'GET'])
@login_required
def employees_page():
    """
    Function working on employees page:
        1) adding new employees session is used by admin
        2) Finding employees by dates of birth
    :return: the template of the employees page
    """

    departments = Departments.query.all()
    employees = Employees.query.all()
    if session.get('user') == ADMIN:
        if request.method == 'POST':
            name = request.form.get('name')
            department = request.form.get('department')
            salary = request.form.get('salary')
            birth_date = request.form.get('birth_date')

            from_date = request.form.get('From')
            to_date = request.form.get('To')

            if name and department and salary and birth_date:
                try:
                    salary = float(salary)
                    if salary<=0:
                        raise ValueError
                    birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
                    add_emp(name, department, salary, birth_date)
                except:
                    pass
                return redirect('/employees')
            elif from_date and to_date:
                try:
                    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
                    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
                    if to_date >= from_date:
                        employees = find_emp(from_date, to_date)
                except:
                    pass
        return render_template('employees.html', employees=employees, departments=departments)
    if request.method == 'POST':
        if 'From' in request.form.keys() and 'To' in request.form.keys():
            departments, employees = find_emp(departments, employees)
    return render_template('employees_for_users.html', employees=employees, departments=departments)

@api_employees.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_emp(id):
    """
    Function editing information about specific employee
    :param id: id of the specific employee an admin wants to change information about
    :return: return template of the departments page or redirects to employees page
    """
    if session.get('user') == ADMIN:
        departments = Departments.query.all()
        employees = Employees.query.all()
        if Employees.query.get(id):
            if request.method == 'POST':
                name = request.form.get('new_name')
                department = request.form.get('new_department')
                salary = request.form.get('new_salary')
                birth_date = request.form.get('new_birth_date')
                if name and department and salary and birth_date:
                    try:
                        salary = float(salary)
                        if salary <= 0:
                            raise ValueError
                        birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
                        change_emp(id, name, department, salary, birth_date)
                    except:
                        pass
                return redirect('/employees')
            return render_template('employees.html', id=id, departments=departments, employees=employees)
        return redirect('/employees')

@api_employees.route('/employees/<int:id>/del')
@login_required
def delete_emp(id):
    """
    Function deleting specific employee by its id
    :param id: id of the specific employee an admin wants to delete
    :return: redirects to the employees page
    """
    if session.get('user') == ADMIN:
        del_emp(id)
        return redirect('/employees')




@api_employees.before_request
def check_session():
    users = User.query.filter_by(login=session.get('user')).all()
    if users:
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')