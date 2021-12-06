"""
Module contains classes to work with REST API for Employees.

Classes:
    DepartmentsAPIget(Resource)
    DepartmentsAPIadd(Resource)
    DepartmentsAPIedit(Resource)
    DepartmentsAPIdel(Resource)
"""
from flask_restful import Resource, abort, reqparse
from flask import redirect
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))
from .common_funcs import check_empty_strings
from models.users import User
from models.departments import Departments
from models.employees import Employees
from migrations.migrations_funcs import avg_salaries
from service import add_dnt, change_dnt, del_dnt
from f_logger import logger

get_args = reqparse.RequestParser()
get_args.add_argument("login", type=str, help="User`s login", required=True)
get_args.add_argument("password", type=str, help="User`s password", required=True)

add_args = reqparse.RequestParser()
add_args.add_argument("login", type=str, help="User`s login", required=True)
add_args.add_argument("password", type=str, help="User`s password", required=True)
add_args.add_argument("department", type=str, help="Name of new department", required=True)
add_args.add_argument("page", type=str, help="Redirects to prev page")

edit_args = reqparse.RequestParser()
edit_args.add_argument("login", type=str, help="User`s login", required=True)
edit_args.add_argument("password", type=str, help="User`s password", required=True)
edit_args.add_argument("department", type=str, help="New name of the department", required=True)
edit_args.add_argument("id", type=int, help="Id of the department to edit", required=True)
edit_args.add_argument("page", type=str, help="Redirects to prev page")

del_args = reqparse.RequestParser()
del_args.add_argument("login", type=str, help="User`s login", required=True)
del_args.add_argument("password", type=str, help="User`s password", required=True)
del_args.add_argument("id", type=int, help="Id of the department to delete", required=True)
del_args.add_argument("page", type=str, help="Redirects to prev page")


class DepartmentsAPIget(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for giving info about departments of the table.

    Methods:
        get(self)
    """

    def get(self):
        """
        Method overrides get method of Resource and
        works on get method, giving info about departments,
        only if credentials are correct.
        :return: dict of user information
        """
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
    """
    Class ,which is descendant of Resource, is responsible
    for adding departments to the table.

    Methods:
        get(self)
    """

    def get(self):
        """
         Method overrides get method of Resource and
         works on get method, adding departments,
         only if arguments and credentials are correct.
         :return: dict of messages or errors
        """
        args = add_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        department = args['department']
        page = args.get('page')
        if user and user.password == password and user.id == 1:
            if check_empty_strings(department) and not Departments.query.filter_by(department=department).first():
                add_dnt(department)
                logger.info(f'Added department: "{department}"')
                if page and page == 'True':
                    return redirect('/departments')
                return {'message': 'ADD_SUCCESS'}
            logger.info(f'Failed adding department: "{department}"')
            if page and page == 'True':
                return redirect('/departments')
            abort(401, error='ARGUMENTS_INCORRECT')
        logger.info(f'Failed adding employee: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class DepartmentsAPIedit(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for editing departments of the table.

    Methods:
        get(self)
    """

    def get(self):
        """
         Method overrides get method of Resource and
         works on get method, editing departments,
         only if arguments and credentials are correct.
         :return: dict of messages or errors
        """
        args = edit_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        department = args['department']
        id = args['id']
        page = args.get('page')
        if user and user.password == password and user.id == 1:
            if check_empty_strings(department) and Departments.query.get(id) \
                    and (not Departments.query.filter_by(department=department).first()
                         or Departments.query.get(id).department == department):
                change_dnt(id, department)
                logger.info(f'Edited department: id: "{id}"\tdepartment: "{department}"')
                if page and page == 'True':
                    return redirect('/departments')
                return {'message': 'EDIT_SUCCESS'}
            logger.info(f'Failed editing department: id: "{id}"\tdepartment: "{department}"')
            if page and page == 'True':
                return redirect('/departments')
            abort(401, error='ARGUMENTS_INCORRECT')
        logger.info(f'Failed editing employee: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class DepartmentsAPIdel(Resource):
    """
    Class ,which is descendant of Resource, is responsible
    for deleting departments from the table.

    Methods:
        get(self)
    """

    def get(self):
        """
         Method overrides get method of Resource and
         works on get method, deleting departments,
         only if arguments and credentials are correct.
         :return: dict of messages or errors
        """
        args = del_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        id = args['id']
        page = args.get('page')
        if user and user.password == password and user.id == 1:
            if Departments.query.get(id) and id != 1:
                del_dnt(id)
                logger.info(f'Deleted department: id: "{id}"')
                if page and page == 'True':
                    return redirect('/departments')
                return {'message': 'DEL_SUCCESS'}
            logger.info(f'Failed deleting department: id: "{id}"')
            if page and page == 'True':
                return redirect('/departments')
            abort(406, error='ARGUMENTS_INCORRECT')
        logger.info(f'Failed deleting employee: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')
