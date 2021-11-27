import os
import sys
import datetime
from flask_login import login_user, login_required, logout_user

sys.path.append(os.path.abspath(os.path.join('..')))

from models.employees import Employees
from models.departments import Departments
from models.users import User
from flask import Flask, render_template, request, redirect, Blueprint, flash, url_for, session
from service import avg_salaries, add_emp, add_dnt, find_emp, change_emp, change_dnt, \
    del_dnt, del_emp, add_user, del_user, change_user
from werkzeug.security import check_password_hash

ADMIN = User.query.get(1).login
api = Blueprint('api', __name__)


@api.route('/', methods=['GET', 'POST'])
def login_page():
    """
    Function returning the template of the main page
    :return: the template of the main page
    """
    logout_user()
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.password == password:
                login_user(user)
                session['user'] = login
                next_page = request.args.get('next')
                return redirect('/departments')
            else:
                flash('Login or password is not correct')
        else:
            flash('Please, fill login and password fields')
    return render_template('index.html')


@api.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect('/')


@api.before_request
def make_session_permanent():
    session.permanent = False


@api.after_request
def redirect_to_sign_in(response):
    if response.status_code == 401:
        return redirect(url_for('api.login_page') + '?next=' + request.url)
    return response


@api.route('/users', methods=['POST', 'GET'])
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
    user = User.query.filter_by(login=session.get('user')).first()
    return render_template('users.html', user=user)


@api.route('/departments', methods=['POST', 'GET'])
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
            if department and not Departments.query.filter_by(department=department):
                add_dnt(department)
            return redirect('/departments')
        return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)
    return render_template('departments_for_users.html', departments=departments, dnt_salary=dnt_salary)


@api.route('/employees', methods=['POST', 'GET'])
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
                add_emp(name, department, salary, birth_date)
                return redirect('/employees')
            elif from_date and to_date:
                employees = find_emp(from_date, to_date)
        return render_template('employees.html', employees=employees, departments=departments)
    if request.method == 'POST':
        if 'From' in request.form.keys() and 'To' in request.form.keys():
            departments, employees = find_emp(departments, employees)
    return render_template('employees_for_users.html', employees=employees, departments=departments)


@api.route('/users/<int:id>/del')
@login_required
def delete_user(id):
    """
    Function deleting specific user by its id
    :param id: id of the specific user an admin wants to delete
    :return: redirects user to the users page
    """
    if session.get('user') == ADMIN:
        if User.query.get_or_404(id).login != ADMIN:
            del_user(id)
        return redirect('/users')


@api.route('/departments/<int:id>/del')
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


@api.route('/employees/<int:id>/del')
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


@api.route('/users/<int:id>/edit', methods=['GET', 'POST'])
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
                change_user(id)
                return redirect('/users')

            return render_template('users_for_admin.html', id=id, users=users)
        else:
            return redirect('/users')


@api.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
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
                change_emp(id)
                return redirect('/employees')

            return render_template('employees.html', id=id, departments=departments, employees=employees)
        else:
            return redirect('/employees')


@api.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
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
                change_dnt(id)
                return redirect('/departments')
            return render_template('departments.html', id=id, departments=departments, dnt_salary=dnt_salary)
        else:
            return redirect('/departments')
