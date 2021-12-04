from flask_restful import Resource, abort, reqparse
import os
import sys
import datetime


sys.path.append(os.path.abspath(os.path.join('..')))
from .common_funcs import check_empty_strings
from models.users import User
from models.departments import Departments
from models.employees import Employees

from service import add_emp, find_emp, change_emp, del_emp

get_args = reqparse.RequestParser()
get_args.add_argument("login", type=str, help="User`s login", required=True)
get_args.add_argument("password", type=str, help="User`s password", required=True)

add_args = reqparse.RequestParser()
add_args.add_argument("login", type=str, help="User`s login", required=True)
add_args.add_argument("password", type=str, help="User`s password", required=True)
add_args.add_argument("name", type=str, help="Name of new employee", required=True)
add_args.add_argument("department", type=str, help="Department of new employee", required=True)
add_args.add_argument("salary", type=float, help="Salary of new employee", required=True)
add_args.add_argument("birth_date", type=str, help="Birthdate of new employee", required=True)

find_args = reqparse.RequestParser()
find_args.add_argument("login", type=str, help="User`s login", required=True)
find_args.add_argument("password", type=str, help="User`s password", required=True)
find_args.add_argument("from_date", type=str, help="Format: YYYY-mm-dd. Date from which employee is sought",
                       required=True)
find_args.add_argument("to_date", type=str, help="Format: YYYY-mm-dd. Date till which employee is sought",
                       required=True)

edit_args = reqparse.RequestParser()
edit_args.add_argument("login", type=str, help="User`s login", required=True)
edit_args.add_argument("password", type=str, help="User`s password", required=True)
edit_args.add_argument("name", type=str, help="New name of the employee", required=True)
edit_args.add_argument("department", type=str, help="New department of the employee", required=True)
edit_args.add_argument("salary", type=float, help="New salary of the employee", required=True)
edit_args.add_argument("birth_date", type=str, help="New birthdate of the employee", required=True)
edit_args.add_argument("id", type=int, help="Id of the employee to edit", required=True)

del_args = reqparse.RequestParser()
del_args.add_argument("login", type=str, help="User`s login", required=True)
del_args.add_argument("password", type=str, help="User`s password", required=True)
del_args.add_argument("id", type=int, help="Id of the employee to delete", required=True)


class EmployeesAPIget(Resource):
    def post(self):
        args = get_args.parse_args()
        login = args['login']
        password = args['password']
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


class EmployeesAPIadd(Resource):
    def post(self):
        args = add_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password and user.id == 1:
            name = args['name']
            department = args['department']
            salary = args['salary']
            birth_date = args['birth_date']
            if Departments.query.filter_by(department=department).first():
                try:
                    if check_empty_strings(name) and salary > 0:
                        birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
                        add_emp(name, department, salary, birth_date)
                        return {'message': 'ADD_SUCCESS'}
                    raise ValueError
                except ValueError:
                    abort(406, error='ARGUMENTS_INCORRECT')
            abort(406, error='NO_SUCH_DEPARTMENT_EXISTS')
        abort(401, error='CREDENTIALS_INCORRECT')


class EmployeesAPIfind(Resource):
    def post(self):
        args = find_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password:
            from_date = args['from_date']
            to_date = args['to_date']
            try:
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
                raise ValueError
            except ValueError:
                abort(406, error='ARGUMENTS_INCORRECT')
        abort(401, error='CREDENTIALS_INCORRECT')


class EmployeesAPIedit(Resource):
    def post(self):
        args = edit_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password and user.id == 1:
            name = args['name']
            department = args['department']
            salary = args['salary']
            birth_date = args['birth_date']
            id = args['id']
            if Employees.query.get(id):
                if Departments.query.filter_by(department=department).first():
                    try:
                        if check_empty_strings(name) and salary > 0:
                            birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
                            change_emp(id, name, department, salary, birth_date)
                            return {'message': 'EDIT_SUCCESS'}
                        raise ValueError
                    except ValueError:
                        abort(406, error='ARGUMENTS_INCORRECT')
                abort(406, error='NO_SUCH_DEPARTMENT_EXISTS')
            abort(406, error='NO_SUCH_ID')
        abort(401, error='CREDENTIALS_INCORRECT')


class EmployeesAPIdel(Resource):
    def post(self):
        args = del_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password and user.id == 1:
            id = args['id']
            if Employees.query.get(id):
                del_emp(id)
                return {'message': 'DEL_SUCCESS'}
            abort(406, error='NO_SUCH_ID')
        abort(401, error='CREDENTIALS_INCORRECT')
