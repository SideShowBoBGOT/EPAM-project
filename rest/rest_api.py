from flask import Flask, request
from flask_restful import Api, Resource, abort
import os
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join('..')))

from application import db
from models.employees import Employees
from models.departments import Departments
from models.users import User

from service import avg_salaries, add_emp, add_dnt, find_emp, change_emp, change_dnt, \
    del_dnt, del_emp, add_user, del_user, change_user

r_api = Api()


class UserAPI(Resource):
    def get(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.password == password:
                # admin`s id is 1
                if user.id == 1 and user.password == password:
                    users = dict()
                    for usr in User.query.all():
                        users[usr.id] = {'id': usr.id, 'login': usr.login,
                                         'password': usr.password}
                    return users
                return {'id': user.id, 'login': user.login,
                        'password': user.password}
        abort(401, error='CREDENTIALS_INCORRECT')

    def post(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            # admin`s id is 1
            if user and user.id == 1 and user.password == password:
                user_login = request.form.get('login')
                user_password = request.form.get('password')
                id = request.form.get('id')
                func = request.form.get('func')
                if func == 'add' and user_login and user_password:
                    if not User.query.filter_by(login=user_login).first():
                        add_user(user_login, user_password)
                        return {'message': 'ADD_SUCCESS'}
                    abort(404, error='LOGIN_ALREADY_USED')
                elif func == 'edit' and user_login \
                        and user_password and id and User.query.get(id):
                    if not User.query.filter_by(login=user_login).first() or User.query.get(id).login == user_login:
                        change_user(id, user_login, user_password)
                        return {'message': 'EDIT_SUCCESS'}
                    abort(404, error='LOGIN_ALREADY_USED')
                elif func == 'del' and id:
                    if id != 1:
                        del_user(id)
                        return {'message': 'DEL_SUCCESS'}
                    abort(406, error='ADMIN_UNDELETABLE')
                abort(406, error='ARGUMENTS_INCORRECT')
        abort(401, error='CREDENTIALS_INCORRECT')


r_api.add_resource(UserAPI, '/api/<string:login>/<string:password>/users')


class DepartmentsAPI(Resource):
    def get(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.password == password:
                departments_dict = dict()
                departments = Departments.query.all()
                employees = Employees.query.all()
                dnt_salary = avg_salaries(departments, employees)
                for index, dnt in enumerate(departments):
                    departments_dict[f'{index}'] = {'id': dnt.id, 'department': dnt.department,
                                                    'avg_salary': dnt_salary[dnt.department]}
                return departments_dict
        abort(401, error='CREDENTIALS_INCORRECT')

    def post(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            # admin`s id is 1
            if user and user.id == 1 and user.password == password:
                department = request.form.get('department')
                id = request.form.get('id')
                func = request.form.get('func')
                if func == 'add' and department:
                    if not Departments.query.filter_by(department=department).first():
                        add_dnt(department)
                        return {'message': 'ADD_SUCCESS'}
                    abort(406, error='DNT_NAME_ALREADY_USED')
                elif func == 'edit' and department and id and Departments.query.get(id):
                    if not Departments.query.filter_by(department=department).first() or\
                            Departments.query.get(id).department == department:
                        change_dnt(id, department)
                        return {'message': 'EDIT_SUCCESS'}
                    abort(406, error='DNT_NAME_ALREADY_USED')
                elif func == 'del' and id:
                    del_dnt(id)
                    return {'message': 'DEL_SUCCESS'}
                abort(406, error='ARGUMENTS_INCORRECT')
        abort(401, error='CREDENTIALS_INCORRECT')


r_api.add_resource(DepartmentsAPI, '/api/<string:login>/<string:password>/departments')


class EmployeesAPI(Resource):
    def get(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.password == password:
                employees_dict = dict()
                employees = Employees.query.all()
                for index, emp in enumerate(employees):
                    employees_dict[f'{index}'] = {'id': emp.id, 'name': emp.name,
                                                  'department': emp.department,
                                                    'salary': emp.salary,
                                                  'birth_date': str(emp.birth_date)}
                return employees_dict
        abort(401, error='CREDENTIALS_INCORRECT')

    def post(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            # admin`s id is 1
            if user and user.password == password:
                name = request.form.get('name')
                department = request.form.get('department')
                salary = request.form.get('salary')
                birth_date = request.form.get('birth_date')

                from_date = request.form.get('From')
                to_date = request.form.get('To')
                id = request.form.get('id')
                func = request.form.get('func')

                if func == 'find' and from_date and to_date:
                    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
                    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
                    if to_date >= from_date:
                        employees = find_emp(from_date, to_date)
                        employees_dict = dict()
                        for index, emp in enumerate(employees):
                            employees_dict[f'{index}'] = {'id': emp.id, 'name': emp.name,
                                                          'department': emp.department,
                                                          'salary': emp.salary,
                                                          'birth_date': str(emp.birth_date)}
                        return employees_dict
                    abort(406, error='DATES_INCORRECT')
                if user.id == 1:
                    if func == 'add' and name and department and salary and birth_date:
                        if Departments.query.filter_by(department=department).first():
                            add_emp(name, department, salary, birth_date)
                            return {'message': 'ADD_SUCCESS'}
                        abort(406, error='NO_SUCH_DEPARTMENT_EXISTS')
                    elif func == 'edit' and name and department and salary and birth_date and\
                            id and Employees.query.get(id):
                        if Departments.query.filter_by(department=department).first():
                            change_emp(id, name, department, salary, birth_date)
                            return {'message': 'EDIT_SUCCESS'}
                        abort(406, error='NO_SUCH_DEPARTMENT_EXISTS')
                    elif func == 'del' and id:
                        del_emp(id)
                        return {'message': 'DEL_SUCCESS'}
                    abort(406, error='ARGUMENTS_INCORRECT')
        abort(401, error='CREDENTIALS_INCORRECT')


r_api.add_resource(EmployeesAPI, '/api/<string:login>/<string:password>/employees')