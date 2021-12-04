import os
import sys
import unittest
import datetime
import json

sys.path.append(os.path.abspath(os.path.join('..')))

from models.departments import Departments
from models.employees import Employees
from models.users import User
from wsgi import app

app.app_context().push()
ADMIN_LOGIN = User.query.get(1).login
ADMIN_PASSWORD = User.query.get(1).password


class FlaskTestCases(unittest.TestCase):
    # Ensure server responds correctly to employees get API request
    def test_employees_api_get(self):
        tester = app.test_client(self)
        response = tester.post('/api/employees/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        self.assertTrue(Employees.query.all()[0].department.encode() in response.data)

    # Ensure server responds correctly to employees add API request given correct args
    def test_employees_api_add(self):
        tester = app.test_client(self)
        name = 'dsjfbewibfbibwsfwefpmewnoiq[],xmv'
        department = Departments.query.all()[0].department
        birth_date = datetime.datetime.now().date()
        salary = 50000
        response = tester.post('/api/employees/add', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                               name=name, department=department,
                                                               birth_date=birth_date, salary=salary),
                               follow_redirects=True)
        response = tester.post('/api/employees/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        self.assertTrue(name.encode() in response.data)
        self.assertTrue(department.encode() in response.data)
        self.assertTrue(str(birth_date).encode() in response.data)
        self.assertTrue(str(salary).encode() in response.data)
        response = response = tester.post('/api/employees/del', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                                          id=Employees.query.all()[-1].id),
                                          follow_redirects=True)

    # Ensure server responds correctly to employees add API request given incorrect args
    def test_employees_add_err(self):
        tester = app.test_client(self)
        prev_employees = Employees.query.all()
        login_vars = (None, '', 'incorrect', User.query.all()[0].login)
        password_vars = (None, '', 'incorrect', User.query.all()[0].password)
        name_states = (None, 'askdiuqwebhbvchsf ehasfuywbb')
        department_states = (None, Departments.query.all()[0].department)
        birth_date_states = (None, '1978-9-10')
        salary_states = (None, -19230, '*sdf111', 11000)
        variations = []
        for login in login_vars:
            for password in password_vars:
                for ns in name_states:
                    for ds in department_states:
                        for bs in birth_date_states:
                            for ss in salary_states:
                                variations.append((login, password, ns, ds, bs, ss))
        for variation in variations[:-1]:
            response = tester.post('/api/employees/add', data=dict(login=variation[0], password=variation[1],
                                                                   name=variation[2], department=variation[3],
                                                                   birth_date=variation[4], salary=variation[5]),
                                   follow_redirects=True)
            new_employees = Employees.query.all()
            self.assertTrue(prev_employees == new_employees)

    # Ensure server responds correctly to employees edit API request given correct args
    def test_employees_api_edit(self):
        tester = app.test_client(self)
        prev_name = 'dsjfbewibfbibwsfwefpmewnoiq[],xmv'
        prev_department = Departments.query.all()[0].department
        prev_birth_date = datetime.datetime.now().date()
        prev_salary = 50000
        response = tester.post('/api/employees/add', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                               name=prev_name, department=prev_department,
                                                               birth_date=prev_birth_date, salary=prev_salary),
                               follow_redirects=True)

        name = '..ds,.,vjalnvcsd[]qle]]ql,  mnkmcv,;q[l'
        department = Departments.query.all()[-1].department
        birth_date = '1999-09-09'
        salary = 7777
        id = Employees.query.all()[-1].id
        response = tester.post('/api/employees/edit', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                                name=name, department=department,
                                                                birth_date=birth_date, salary=salary,
                                                                id=id),
                               follow_redirects=True)
        response = tester.post('/api/employees/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        self.assertTrue(name.encode() in response.data)
        self.assertTrue(department.encode() in response.data)
        self.assertTrue(str(birth_date).encode() in response.data)
        self.assertTrue(str(salary).encode() in response.data)
        response = tester.post('/api/employees/del', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD, id=id),
                               follow_redirects=True)

    # Ensure server responds correctly to employees edit API request given incorrect args
    def test_employees_api_edit_err(self):
        tester = app.test_client(self)
        login = 'sdlkfnkslodnfalfnalfndsfakfoeipwn eworf'
        password = 'dsjkfnoq-302-032refsdfsdnmpdos[pmpksd'
        response = tester.post('/api/employeess/add', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                                new_login=login, new_password=password),
                               follow_redirects=True)
        old_response = tester.post('/api/employeess/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                                   follow_redirects=True)
        login_vars = (None, '', 'incorrect', User.query.all()[0].login)
        password_vars = (None, '', 'incorrect', User.query.all()[0].password)
        name_states = (None, 'askdiuqwebhbvchsf ehasfuywbb')
        department_states = (None, Departments.query.all()[0].department)
        birth_date_states = (None, '1978-9-10')
        salary_states = (None, -19230, '*sdf111', 11000)
        id_vars = (None, '', '3s', -1, Employees.query.all()[-1].id)
        variations = []
        for login in login_vars:
            for password in password_vars:
                for ns in name_states:
                    for ds in department_states:
                        for bs in birth_date_states:
                            for ss in salary_states:
                                for id in id_vars:
                                    variations.append((login, password, ns, ds, bs, ss, id))
        for variation in variations[:-1]:
            response = tester.post('/api/employees/edit', data=dict(login=variation[0], password=variation[1],
                                                                    name=variation[2], department=variation[3],
                                                                    birth_date=variation[4], salary=variation[5],
                                                                    id=variation[6]),
                                   follow_redirects=True)
            new_response = tester.post('/api/employeess/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                                       follow_redirects=True)
            self.assertTrue(old_response.data == new_response.data)
        id = Employees.query.all()[-1].id
        response = tester.post('/api/employeess/del', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD, id=id),
                               follow_redirects=True)

    # Ensure server responds correctly to employees del API request given correct args
    def test_employeess_api_del(self):
        tester = app.test_client(self)
        old_response = tester.post('/api/employeess/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                                   follow_redirects=True)
        name = 'dsjfbewibfbibwsfwefpmewnoiq[],xmv'
        department = Departments.query.all()[0].department
        birth_date = datetime.datetime.now().date()
        salary = 50000
        response = tester.post('/api/employees/add', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                               name=name, department=department,
                                                               birth_date=birth_date, salary=salary),
                               follow_redirects=True)
        id = Employees.query.all()[-1].id
        response = tester.post('/api/employeess/del', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD, id=id),
                               follow_redirects=True)
        new_response = tester.post('/api/employeess/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                                   follow_redirects=True)
        self.assertTrue(old_response.data == new_response.data)

    # Ensure server responds correctly to employees del API request given incorrect args
    def test_employeess_api_del_err(self):
        tester = app.test_client(self)
        old_response = tester.post('/api/employeess/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                                   follow_redirects=True)
        id_vars = (None, '', '3s', -1)
        for id in id_vars:
            response = tester.post('/api/employeess/del', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD, id=id),
                                   follow_redirects=True)
            new_response = tester.post('/api/employeess/get', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                                       follow_redirects=True)
            self.assertTrue(old_response.data == new_response.data)

    # Ensure server responds correctly to employees find API request given correct args
    def test_employees_api_find(self):
        tester = app.test_client(self)
        test_dates = ['1970-12-11', '1973-03-14', '1996-04-19']
        for test_date in test_dates:
            response = tester.post('/api/employees/add', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                                   name='sdfsdfww',
                                                                   department=Departments.query.all()[0].department,
                                                                   birth_date=test_date, salary=1111),
                                   follow_redirects=True)
        from_date = '1970-01-01'
        to_date = '1987-05-06'

        response = tester.post('/api/employees/find',  data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                              from_date=from_date, to_date=to_date),
                                                    follow_redirects=True)
        selected_employees = json.loads(response.data)
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        for value in selected_employees.values():
            date = datetime.datetime.strptime(value['birth_date'], '%Y-%m-%d').date()
            self.assertTrue(from_date<=date<=to_date)
        for i in range(3,0,-1):
            id = Employees.query.all()[-i].id
            response = tester.post('/api/employees/del', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD, id=id),
                                   follow_redirects=True)

    # Ensure server responds correctly to employees find API request given incorrect args
    def test_employees_api_find_err(self):
        tester = app.test_client(self)
        from_date_states = (None, '', 23222, '2020-24-30')
        to_date_states = from_date_states
        for from_date in from_date_states:
            for to_date in to_date_states:
                response = tester.post('/api/employees/find', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD,
                                                                        from_date=from_date, to_date=to_date),
                                       follow_redirects=True)
                response_dict = json.loads(response.data)
                self.assertTrue('error' in response_dict.keys() or 'message' in response_dict.keys())

