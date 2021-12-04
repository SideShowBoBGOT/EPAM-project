from flask_restful import Resource, abort, reqparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))
from .common_funcs import check_empty_strings
from models.users import User
from models.departments import Departments
from models.employees import Employees
from service import avg_salaries, add_dnt, change_dnt, del_dnt
from f_logger import logger

get_args = reqparse.RequestParser()
get_args.add_argument("login", type=str, help="User`s login", required=True)
get_args.add_argument("password", type=str, help="User`s password", required=True)

add_args = reqparse.RequestParser()
add_args.add_argument("login", type=str, help="User`s login", required=True)
add_args.add_argument("password", type=str, help="User`s password", required=True)
add_args.add_argument("department", type=str, help="Name of new department", required=True)

edit_args = reqparse.RequestParser()
edit_args.add_argument("login", type=str, help="User`s login", required=True)
edit_args.add_argument("password", type=str, help="User`s password", required=True)
edit_args.add_argument("department", type=str, help="New name of the department", required=True)
edit_args.add_argument("id", type=int, help="Id of the department to edit", required=True)

del_args = reqparse.RequestParser()
del_args.add_argument("login", type=str, help="User`s login", required=True)
del_args.add_argument("password", type=str, help="User`s password", required=True)
del_args.add_argument("id", type=int, help="Id of the department to delete", required=True)


class DepartmentsAPIget(Resource):
    def post(self):
        args = get_args.parse_args()
        login = args['login']
        password = args['password']
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


class DepartmentsAPIadd(Resource):
    def post(self):
        args = add_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        department = args['department']
        if user and user.password == password and user.id == 1:
            if check_empty_strings(department) and not Departments.query.filter_by(department=department).first():
                add_dnt(department)
                logger.info(f'Added department: "{department}"')
                return {'message': 'ADD_SUCCESS'}
            logger.info(f'Failed adding department: "{department}"')
            abort(401, error='ARGUMENTS_INCORRECT')
        logger.info(f'Failed adding employee: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class DepartmentsAPIedit(Resource):
    def post(self):
        args = edit_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password and user.id == 1:
            department = args['department']
            id = args['id']
            if check_empty_strings(department) and Departments.query.get(id) \
                    and (not Departments.query.filter_by(department=department).first()
                         or Departments.query.get(id).department == department):
                change_dnt(id, department)
                logger.info(f'Edited department: id: "{id}"\tdepartment: "{department}"')
                return {'message': 'EDIT_SUCCESS'}
            logger.info(f'Failed editing department: id: "{id}"\tdepartment: "{department}"')
            abort(401, error='ARGUMENTS_INCORRECT')
        logger.info(f'Failed editing employee: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class DepartmentsAPIdel(Resource):
    def post(self):
        args = del_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password and user.id == 1:
            id = args['id']
            if Departments.query.get(id) and id != 1:
                del_dnt(id)
                logger.info(f'Deleted department: id: "{id}"')
                return {'message': 'DEL_SUCCESS'}
            logger.info(f'Failed deleting department: id: "{id}"')
            abort(406, error='ARGUMENTS_INCORRECT')
        logger.info(f'Failed deleting employee: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')
