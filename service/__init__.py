import datetime
import os
import sys

from flask import request
from flask_login import login_user

sys.path.append(os.path.abspath(os.path.join('..')))

from application import db
from models.employees import Employees
from models.departments import Departments
from models.users import User
from werkzeug.security import generate_password_hash






def avg_salaries(departments, employees):
    """
    Function calculating average salary of every department
    :param departments: list of departments in the db
    :param employees: list of employees in the db
    :return: dnt_salary: the dictionary of names of departments as keys and average salaries as values
    """
    dnt_salary = {}
    for dnt in departments:
        dnt_salary[dnt.department] = []
    for emp in employees:
        for dnt in departments:
            if emp.department == dnt.department:
                dnt_salary[dnt.department].append(emp.salary)
    for dnt_name in dnt_salary:
        avg_salary = None
        if dnt_salary[dnt_name]:
            avg_salary = 0
            for salary in dnt_salary[dnt_name]:
                avg_salary += salary
            avg_salary /= len(dnt_salary[dnt_name])
            dnt_salary[dnt_name] = round(avg_salary, 3)
        else:
            avg_salary = 'No employees'
            dnt_salary[dnt_name] = avg_salary

    return dnt_salary

def add_user():
    """
        Function adding new user
        :return: None
        """
    login = request.form['login']
    password = request.form['password']
    already_exists = False
    if login and password:
        for user in User.query.all():
            if login == user.login:
                already_exists = True
        if not already_exists:
            try:
                user = User(login=login, password=password)

                db.session.add(user)
                db.session.commit()
            except:
                print('Error working with adding user')
    return None

def add_emp():
    """
    Function adding new employee to specific department
    :return: None
    """
    try:
        name = request.form['name']
        department = request.form['department']
        salary = int(request.form['salary'])
        birth_date = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        if salary >= 0:
            emp = Employees(name=name, department=department, birth_date=birth_date, salary=salary)

            db.session.add(emp)
            db.session.commit()
    except:
        print('Error working with adding employee')
    return None


def add_dnt():
    """
    Function adding new department to the db
    :return: None
    """
    department = request.form['department']
    already_exists = False
    if department:
        for dnt in Departments.query.all():
            if dnt.department == department:
                already_exists = True
                break
        if not already_exists:
            new_dnt = Departments(department=department)
            try:
                db.session.add(new_dnt)
                db.session.commit()
            except:
                print('Error working with adding department')
    return None



def find_emp(departments, employees):
    """
    Function finding employee between a certain period of time
    :param departments: list of departments in the db
    :param employees: list of employees in the db
    :return: if no errors : list of employees born on certain date ,
            else: unchanged list of employees
    """
    try:
        from_date = datetime.datetime.strptime(request.form['From'], '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(request.form['To'], '%Y-%m-%d').date()
        sorted_employees = []
        if to_date >= from_date:
            for emp in employees:
                if from_date <= emp.birth_date <= to_date:
                    sorted_employees.append(emp)
            return departments, sorted_employees
        else:
            return departments, employees
    except:
        return departments, employees


def change_emp(id):
    """
    Function changing employee`s information
    :param id: id of the employee a user wants to change
    :return: None
    """
    try:
        name = request.form['new_name']
        department = request.form['new_department']
        salary = int(request.form['new_salary'])
        birth_date = datetime.datetime.strptime(request.form['new_birth_date'], '%Y-%m-%d')
        if salary >= 0:
            emp = Employees.query.get_or_404(id)
            emp.name = name
            emp.department = department
            emp.salary = salary
            emp.birth_date = birth_date

            db.session.commit()
    except:
        print('Error working with changing employee')
    return None

def change_user(id):
    """
    Function changing users information
    :param id: id of the user an admin wants to change
    :return: None
    """
    try:
        login = request.form['new_login']
        password = request.form['new_password']

        user = User.query.get_or_404(id)
        user.login = login
        user.password = password

        db.session.commit()
    except:
        print('Error working with changing user')
    return None

def change_dnt(employees, id):
    """
    Function changing information of department
    :param employees: list of employees in the db
    :param id: id of the department a user wants to change
    :return: None
    """
    try:
        dnt = Departments.query.get_or_404(id)
        new_name_dnt = request.form['new_department']
        is_already_exists = False
        if new_name_dnt:
            for d in Departments.query.all():
                if d.department == new_name_dnt and d.id != dnt.id:
                    is_already_exists = True
                    break
            if not is_already_exists:

                    for emp in employees:
                        if emp.department == dnt.department:
                            emp.department = new_name_dnt
                    dnt.department = new_name_dnt

                    db.session.commit()
    except:
        print('Error working with changing department')
    return None

def del_user(id):
    """
    Function deleting user from db
    :param id: if of the user
    :return: None
    """
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        print('Error working with deleting user')
    return None

def del_dnt(employees, id):
    """
    Function deleting department from db
    :param employees: list of employees
    :param id: if of the department
    :return: None
    """
    dnt = Departments.query.get_or_404(id)
    try:
        db.session.delete(dnt)
        for emp in employees:
            if emp.department == dnt.department:
                db.session.delete(emp)
        db.session.commit()
    except:
        print('Error working with deleting department')
    return None

def del_emp(id):
    """
    Function deleting employee from db
    :param id: if of the employee
    :return: None
    """
    emp = Employees.query.get_or_404(id)
    try:
        db.session.delete(emp)
        db.session.commit()
    except:
        print('Error working with deleting employee')
    return None