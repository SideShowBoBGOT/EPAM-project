from flask import Flask, request
from flask_restful import Api, Resource
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from application import db
from models.employees import Employees
from models.departments import Departments
from models.users import User

from service import avg_salaries, add_emp, add_dnt, find_emp, change_emp, change_dnt, \
    del_dnt, del_emp, add_user, del_user, change_user

r_api = Api()


class UserAPI(Resource):
    def get(self):
        users = dict()
        for user in User.query.all():
            users[user.id] = {'login': user.login,
                              'password': user.password}
        return users


r_api.add_resource(UserAPI, '/users')


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
        return {'error': 'CREDENTIALS_INCORRECT'}

    def post(self, login, password):
        if login and password:
            user = User.query.filter_by(login=login).first()
            # admin`s id is 1
            if user and user.id == 1 and user.password == password:
                if request.form['func'] == 'add' and request.form['department']:
                    add_dnt()
                    return {'message': 'ADD_SUCCESS'}
                elif request.form['func'] == 'edit' and request.form['new_department'] and request.form['id']:
                    change_dnt(request.form['id'])
                elif request.form['func'] == 'del'and request.form['ss']:
                    pass
                return {'error': 'ARGUMENTS_INCORRECT'}


r_api.add_resource(DepartmentsAPI, '/api/<string:login>/<string:password>/departments')



class EmployeesAPI(Resource):
    pass
