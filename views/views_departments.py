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
from service import avg_salaries, add_dnt, change_dnt, del_dnt

ADMIN = User.query.get(1).login
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
    if session.get('user') == ADMIN:
        if request.method == 'POST':
            department = request.form.get('department')
            if department and not Departments.query.filter_by(department=department).first():
                add_dnt(department)
            return redirect('/departments')
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
    if session.get('user') == ADMIN:
        del_dnt(id)
        return redirect('/departments')

@api_departments.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_dnt(id):
    """
    Function editing information about specific departments
    :param id:  id of the specific department
    :return: the template of the employees page or redirects to departments
    """
    if session.get('user') == ADMIN:
        departments = Departments.query.all()
        employees = Employees.query.all()
        dnt_salary = avg_salaries(departments, employees)
        if Departments.query.get(id):
            if request.method == 'POST':
                department = request.form.get('new_department')
                if department and \
                        (not Departments.query.filter_by(department=department).first() or
                         Departments.query.get(id).department == department):
                    change_dnt(id, department)
                return redirect('/departments')
            return render_template('departments.html', id=id, departments=departments, dnt_salary=dnt_salary)
        return redirect('/departments')





@api_departments.before_request
def check_session():
    users = User.query.filter_by(login=session.get('user')).all()
    if users:
        login_user(users[0])
        session.permanent = False
    else:
        return redirect('/')