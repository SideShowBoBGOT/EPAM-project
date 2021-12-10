import sys
import unittest
import os

sys.path.append(os.path.abspath(os.path.join('..')))

from models.departments import Departments
from models.users import User
from wsgi import app

app.app_context().push()
ADMIN_LOGIN = User.query.get(1).login
ADMIN_PASSWORD = User.query.get(1).password


class FlaskTestCases(unittest.TestCase):
    # Ensure server responds correctly to departments get API request
    def test_departments_api_get(self):
        tester = app.test_client(self)
        response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                              follow_redirects=True)
        self.assertTrue(Departments.query.all()[0].department.encode() in response.data)

    # Ensure server responds correctly to departments add API request given correct args
    def test_departments_api_add(self):
        tester = app.test_client(self)
        department = 'sadasdasdasd'
        response = tester.get(f'/api/departments/add?login={ADMIN_LOGIN}'
                              f'&password={ADMIN_PASSWORD}&department={department}',
                              follow_redirects=True)
        response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                              follow_redirects=True)
        self.assertTrue(department.encode() in response.data)
        id = Departments.query.all()[-1].id
        response = tester.get(f'/api/departments/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)

    # Ensure server responds correctly to departments add API request given incorrect args
    def test_departments_add_err(self):
        tester = app.test_client(self)
        prev_users_num = Departments.query.all()
        login_vars = ('', 'incorrect', User.query.all()[0].login)
        password_vars = ('', 'incorrect', User.query.all()[0].password)
        department_vars = ('', Departments.query.all()[-1].department)
        variations = []
        for login in login_vars:
            for password in password_vars:
                for department in department_vars:
                    variations.append((login, password, department))
        for variation in variations[:-1]:
            response = tester.get(f'/api/departments/add?login={variation[0]}&password={variation[1]}'
                                  f'&department={variation[2]}', follow_redirects=True)
            new_users_num = Departments.query.all()
            self.assertTrue(prev_users_num == new_users_num)

    # Ensure server responds correctly to departments edit API request given correct args
    def test_departments_api_edit(self):
        tester = app.test_client(self)
        department = 'sdlkfnkslodnfalfnalfndsfakfoeipwn eworf'

        response = tester.get(f'/api/departments/add?login={ADMIN_LOGIN}'
                              f'&password={ADMIN_PASSWORD}&department={department}',
                              follow_redirects=True)
        new_department = 'sdawqmvm]dc sdzzzzzqqq'
        id = Departments.query.all()[-1].id
        response = tester.get(f'/api/departments/edit?login={ADMIN_LOGIN}'
                              f'&password={ADMIN_PASSWORD}&id={id}&department={new_department}',
                              follow_redirects=True)
        response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                              follow_redirects=True)
        self.assertTrue(new_department.encode() in response.data)
        response = tester.get(f'/api/departments/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)

    # Ensure server responds correctly to departments edit API request given incorrect args
    def test_departments_api_edit_err(self):
        tester = app.test_client(self)
        department = 'sdlkfnkslodnfalfnalfndsfakfoeipwn eworf'
        response = tester.get(f'/api/departments/add?login={ADMIN_LOGIN}'
                              f'&password={ADMIN_PASSWORD}&department={department}',
                              follow_redirects=True)
        old_response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        login_vars = (None, '', 'incorrect', User.query.all()[0].login)
        password_vars = (None, '', 'incorrect', User.query.all()[0].password)
        department_vars = (None, '', Departments.query.all()[-1].department)
        id_vars = (None, '', '3s', -1, User.query.all()[-1].id)
        variations = []
        for login in login_vars:
            for password in password_vars:
                for department in department_vars:
                    for id in id_vars:
                        variations.append((login, password, department, id))
        for variation in variations[:-1]:
            response = tester.get(f'/api/departments/edit?login={variation[0]}&password={variation[1]}'
                                  f'&department={variation[2]}&id={variation[3]}',
                                  follow_redirects=True)
            new_response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                      follow_redirects=True)
            self.assertTrue(old_response.data == new_response.data)
        id = Departments.query.all()[-1].id
        response = tester.get(f'/api/departments/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)

    # Ensure server responds correctly to departments del API request given correct args
    def test_departments_api_del(self):
        tester = app.test_client(self)

        old_response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        department = 'sdlkfnkslodnfalfnalfndsfakfoeipwn eworf'
        response = tester.get(f'/api/departments/add?login={ADMIN_LOGIN}'
                              f'&password={ADMIN_PASSWORD}&department={department}',
                              follow_redirects=True)
        id = Departments.query.all()[-1].id
        response = tester.get(f'/api/departments/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)
        new_response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        self.assertTrue(old_response.data == new_response.data)

    # Ensure server responds correctly to departments del API request given incorrect args
    def test_departments_api_del_err(self):
        tester = app.test_client(self)
        old_response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        id_vars = (None, '', '3s', -1)
        for id in id_vars:
            response = tester.get(f'/api/departments/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                                  follow_redirects=True)
            new_response = tester.get(f'/api/departments/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                      follow_redirects=True)
            self.assertTrue(old_response.data == new_response.data)


if __name__ == '__main__':
    unittest.main()
