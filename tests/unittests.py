import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from models.departments import Departments
from models.employees import Employees
from models.users import User

from wsgi import app

app.app_context().push()
import unittest
import datetime
from bs4 import BeautifulSoup

USERS = User.query.all()
ADMIN_LOGIN = User.query.get(1).login
ADMIN_PASSWORD = User.query.get(1).password


class FlaskTestCases(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that admin`s interface is different from public one
    def test_admin_pages(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        self.assertTrue(b'Add department' in response.data)
        response = tester.get('/users', content_type='html/text')
        self.assertTrue(b'Add user' in response.data)
        response = tester.get('/employees', content_type='html/text')
        self.assertTrue(b'Add employee' in response.data)

    # Ensure the user page behaves correctly adding given correct credentials of user
    def test_user_page_add(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        response = tester.get('/users', content_type='html/text')
        new_user_login = 'mechozord'
        new_user_password = 'wquifwbgo[qhpwbqiub221||||'
        response = tester.post('/users', data=dict(login=new_user_login, password=new_user_password),
                               follow_redirects=True)
        self.assertTrue(b'mechozord' in response.data)
        self.assertTrue(b'wquifwbgo[qhpwbqiub221||||' in response.data)

    # Ensure the user page behaves correctly adding given incorrect credentials of user
    def test_user_page_add_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        response = tester.get('/users', content_type='html/text')

        prev_user_num = len(User.query.all())

        # suppose that user inputs login that already exists or None
        user = User.query.all()[-1]
        user_login_states = (None, user.login)
        user_password_states = (None, user.password)
        for log in user_login_states:
            for pasw in user_password_states:
                response = tester.post('/users', data=dict(login=log, password=pasw), follow_redirects=True)
                new_user_num = len(User.query.all())
                self.assertTrue(new_user_num == prev_user_num)

    # Ensure that admin`s interface is different from public one
    def test_common_user_pages(self):
        tester = app.test_client(self)
        user = User.query.all()[-1]
        response = tester.post('/', data=dict(login=user.login, password=user.password),
                               follow_redirects=True)
        self.assertTrue(b'Departments' in response.data)
        response = tester.get('/users', content_type='html/text')
        self.assertTrue(b'Your credentials' in response.data)
        response = tester.get('/employees', content_type='html/text')
        self.assertTrue(b'Employees' in response.data)

    # Ensure the user page behaves correctly editing given correct credentials of user
    def test_user_page_edit(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)

        user_to_edit_id = User.query.all()[-1].id
        login =  User.query.all()[-1].login
        password =  User.query.all()[-1].password
        prev_user_num = len(User.query.all())
        user = User.query.all()[-1]
        new_user_login = 'rararararar'
        new_user_password = 'cmvo[[1]kcmo22q'

        response = tester.post(f'/users/{user_to_edit_id}/edit', data=dict(new_login=new_user_login,
                                                                           new_password=new_user_password),
                               follow_redirects=True)
        user = User.query.all()[-1]
        new_user_num = len(User.query.all())
        self.assertTrue(new_user_num == prev_user_num)
        self.assertTrue(b'rararararar' in response.data)
        self.assertTrue(b'cmvo[[1]kcmo22q' in response.data)
        # set previous login and password
        response = tester.post(f'/users/{user_to_edit_id}/edit', data=dict(new_login=login,
                                                                           new_password=password),
                               follow_redirects=True)

    # Ensure the user page behaves correctly editing given incorrect credentials of user
    def test_user_page_edit_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)

        prev_user_num = len(User.query.all())

        response = tester.get('/users', content_type='html/text')
        user_to_edit_id = User.query.all()[-1].id
        user = User.query.all()[-1]
        user_login_states = (None, user.login)
        user_password_states = (None, user.password)

        for log in user_login_states:
            for pasw in user_password_states:
                response = tester.get(f'/users/{user_to_edit_id}/edit', content_type='html/text')
                response = tester.post(f'/users/{user_to_edit_id}/edit', data=dict(new_login=log,
                                                                                   new_password=pasw),
                                       follow_redirects=True)
                new_user_num = len(User.query.all())
                self.assertTrue(new_user_num == prev_user_num)

    # Ensure the user page behaves correctly canceling changing a user
    def test_user_page_cancel_edit(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = User.query.all()[-1].id
        prev_dnt_num = len(User.query.all())
        response = tester.get(f'/users/{id}/edit', follow_redirects=True)
        response = tester.get('/users')
        new_dnt_num = len(User.query.all())
        self.assertTrue(new_dnt_num == prev_dnt_num)

    # Ensure the user page behaves correctly deleting user
    def test_user_page_del(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = User.query.all()[-1].id
        prev_user_num = len(User.query.all())
        response = tester.get(f'/users/{id}/del', follow_redirects=True)
        new_user_num = len(User.query.all())
        self.assertFalse(prev_user_num == new_user_num)

    # Ensure the departments page behaves correctly given correct name of dnt
    def test_dnt_page_add(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        response = tester.post('/departments', data=dict(department='Go'), follow_redirects=True)
        self.assertTrue(b'Go' in response.data)

    # Ensure the departments page behaves correctly given incorrect name of dnt
    def test_dnt_page_add_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        prev_dnt_num = len(Departments.query.all())
        # 1) suppose that user inputs name of the department that already exists
        for dnt in Departments.query.all():
            response = tester.post('/departments', data=dict(department=dnt.department), follow_redirects=True)
            new_dnt_num = len(Departments.query.all())
            self.assertTrue(new_dnt_num == prev_dnt_num)
        # 2) suppose that user inputs None
        response = tester.post('/departments', data=dict(department=None), follow_redirects=True)
        new_dnt_num = len(Departments.query.all())
        self.assertTrue(new_dnt_num == prev_dnt_num)



    # Ensure the departments page behaves correctly canceling changing a dnt
    def test_dnt_page_cancel_edit(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Departments.query.all()[-1].id
        prev_dnt_num = len(Departments.query.all())
        response = tester.get(f'/departments/{id}/edit', follow_redirects=True)
        response = tester.get('/departments')
        new_dnt_num = len(Departments.query.all())
        self.assertTrue(new_dnt_num == prev_dnt_num)

    # Ensure the departments page behaves correctly changing a dnt given correct name of dnt
    def test_dnt_page_edit(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Departments.query.all()[-1].id
        department = Departments.query.all()[-1].department
        response = tester.post(f'/departments/{id}/edit', data=dict(new_department='Ruby'), follow_redirects=True)
        self.assertTrue(Departments.query.all()[-1].department == 'Ruby')
        #set previous name of department
        response = tester.post(f'/departments/{id}/edit', data=dict(new_department=department), follow_redirects=True)

    # Ensure the departments page behaves correctly changing a dnt given incorrect name of dnt
    def test_dnt_page_edit_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Departments.query.all()[-1].id
        prev_dnt_num = len(Departments.query.all())
        # 1) suppose that user inputs name of the department that already exists
        for dnt in Departments.query.all():
            response = tester.get(f'/departments/{id}/edit', follow_redirects=True)
            response = tester.post(f'/departments/{id}/edit', data=dict(new_department=dnt.department),
                                   follow_redirects=True)
            new_dnt_num = len(Departments.query.all())
            self.assertTrue(new_dnt_num == prev_dnt_num)
        # 2) suppose that user inputs None
        response = tester.get(f'/departments/{id}/edit', follow_redirects=True)
        response = tester.post(f'/departments/{id}/edit', data=dict(new_department=None), follow_redirects=True)
        new_dnt_num = len(Departments.query.all())
        self.assertTrue(new_dnt_num == prev_dnt_num)

    # Ensure the departments page behaves correctly deleting a dnt
    def test_dnt_page_del(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Departments.query.all()[-1].id
        prev_dnt_num = len(Departments.query.all())

        response = tester.get(f'/departments/{id}/del', follow_redirects=True)
        new_dnt_num = len(Departments.query.all())
        self.assertFalse(new_dnt_num == prev_dnt_num)

    # Ensure the employees page behaves correctly adding new emp given correct credentials
    def test_emp_page_add(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        departments = Departments.query.all()
        response = tester.post('/employees', data=dict(name='Marta McDonald', department=departments[0].department,
                                                       birth_date=datetime.datetime.now().date(),
                                                       salary=50000), follow_redirects=True)
        self.assertTrue(b'Marta McDonald' in response.data)

    # Ensure the employees page behaves correctly adding new emp given incorrect credentials
    def test_emp_page_add_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        departments = Departments.query.all()
        prev_emp_num = len(Employees.query.all())
        name_states = (None, 'John Doe')
        department_states = (None, departments[0].department)
        birth_date_states = (None, '1978-9-10')
        salary_states = (None, -19230, '*sdf111', 11000)
        variations_of_input_data = []
        for ns in name_states:
            for ds in department_states:
                for bs in birth_date_states:
                    for ss in salary_states:
                        variations_of_input_data.append((ns, ds, bs, ss))
        # get rid of the last variation ( 'John Doe', departments[0].department, '1978-9-10', 11000) since
        # it is correct
        variations_of_input_data = variations_of_input_data[:-1]
        for variation in variations_of_input_data:
            name = variation[0]
            department = variation[1]
            birth_date = variation[2]
            salary = variation[3]
            response = tester.post('/employees', data=dict(name=name, department=department,
                                                           birth_date=birth_date,
                                                           salary=salary), follow_redirects=True)
            new_emp_num = len(Employees.query.all())
            self.assertTrue(prev_emp_num == new_emp_num)

    # Ensure the employees page behaves correctly finding employees given correct range of dates
    def test_emp_page_find(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        f = '1979-1-10'
        t = '1990-6-5'
        response = tester.post('/employees', data=dict(From=f, To=t), follow_redirects=True)
        From = datetime.datetime.strptime(f, '%Y-%m-%d').date()
        To = datetime.datetime.strptime(t, '%Y-%m-%d').date()
        soup = BeautifulSoup(response.data, 'html.parser')
        found_emps = soup.body.find_next().find_next_siblings()[2].table.tbody.findChildren()

        found_emps = (emp for emp in found_emps if emp.findChildren() and len(emp.findChildren()) > 3)
        dates = (datetime.datetime.strptime(emp.findChildren()[3].text, '%Y-%m-%d').date() for emp in found_emps)
        for date in dates:
            self.assertTrue(From <= date <= To)

    # Ensure the employees page behaves correctly finding employees given incorrect range of dates
    def test_emp_page_find_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        response1 = tester.get('/employees', follow_redirects=True)
        # 1) From > To
        f = '1990-01-10'
        t = '1970-06-05'
        response2 = tester.post('/employees', data=dict(From=f, To=t), follow_redirects=True)
        # if response1 == response2 page has not changed therefore behaves correctly
        self.assertTrue(response1.data == response2.data)
        # 2) From = None
        f = None
        t = '1970-06-05'
        response2 = tester.post('/employees', data=dict(From=f, To=t), follow_redirects=True)
        self.assertTrue(response1.data == response2.data)
        # 3) To = None
        f = '1990-01-10'
        t = None
        response2 = tester.post('/employees', data=dict(From=f, To=t), follow_redirects=True)
        self.assertTrue(response1.data == response2.data)
        # 4) From = None, To = None
        f = None
        t = None
        response2 = tester.post('/employees', data=dict(From=f, To=t), follow_redirects=True)
        self.assertTrue(response1.data == response2.data)



    # Ensure the employees page behaves correctly changing emp given correct credentials
    def test_emp_page_edit(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Employees.query.all()[-1].id
        prev_name = Employees.query.all()[-1].name
        prev_department = Employees.query.all()[-1].department
        prev_birth_date = Employees.query.all()[-1].birth_date
        prev_salary = Employees.query.all()[-1].salary

        name = 'Dan Miron'
        department = Departments.query.all()[-1].department
        birth_date = '1999-09-09'
        salary = 7777
        response = tester.post(f'/employees/{id}/edit', data=dict(new_name=name, new_department=department,
                                                                  new_birth_date=birth_date,
                                                                  new_salary=salary), follow_redirects=True)
        emp = Employees.query.all()[-1]
        self.assertTrue(emp.name == name)
        self.assertTrue(emp.department == department)
        self.assertTrue(str(emp.birth_date) == birth_date)
        self.assertTrue(emp.salary == salary)
        # set to previous attributes
        response = tester.post(f'/employees/{id}/edit', data=dict(new_name=prev_name, new_department=prev_department,
                                                                  new_birth_date=prev_birth_date,
                                                                  new_salary=prev_salary), follow_redirects=True)

    # Ensure the employees page behaves correctly changing emp given incorrect credentials
    def test_emp_page_edit_err(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Employees.query.all()[-1].id
        name_states = (None, 'John Doe')
        department_states = (None, Departments.query.all()[0].department)
        birth_date_states = (None, '1978-9-10')
        salary_states = (None, -19230, '*sdf111', 11000)
        variations_of_input_data = []
        for ns in name_states:
            for ds in department_states:
                for bs in birth_date_states:
                    for ss in salary_states:
                        variations_of_input_data.append((ns, ds, bs, ss))
        # get rid of the last variation ( 'John Doe', departments[0].department, '1978-9-10', 11000) since
        # it is correct
        variations_of_input_data = variations_of_input_data[:-1]
        old_employees = Employees.query.all()
        for variation in variations_of_input_data:
            name = variation[0]
            department = variation[1]
            birth_date = variation[2]
            salary = variation[3]
            response = tester.get(f'/employees/{id}/edit', follow_redirects=True)
            response = tester.post(f'/employees/{id}/edit', data=dict(new_name=name, new_department=department,
                                                                      new_birth_date=birth_date,
                                                                      new_salary=salary), follow_redirects=True)

            # the proof that nothing has changed is that the list of employees has not changed
            new_employees = Employees.query.all()
            for old_emp, new_emp in zip(old_employees, new_employees):
                self.assertTrue(old_emp.name == new_emp.name)
                self.assertTrue(old_emp.department == new_emp.department)
                self.assertTrue(old_emp.birth_date == new_emp.birth_date)
                self.assertTrue(old_emp.salary == new_emp.salary)

    # Ensure the employees page behaves correctly canceling changing emp
    def test_emp_page_cancel_edit(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Employees.query.all()[-1].id
        old_employees = Employees.query.all()
        response = tester.get(f'/employees/{id}/edit', follow_redirects=True)
        response = tester.get('/employees')
        new_employees = Employees.query.all()
        for old_emp, new_emp in zip(old_employees, new_employees):
            self.assertTrue(old_emp.name == new_emp.name)
            self.assertTrue(old_emp.department == new_emp.department)
            self.assertTrue(old_emp.birth_date == new_emp.birth_date)
            self.assertTrue(old_emp.salary == new_emp.salary)

    # Ensure the employees page behaves correctly deleting emp
    def test_emp_page_del(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(login=ADMIN_LOGIN, password=ADMIN_PASSWORD),
                               follow_redirects=True)
        id = Employees.query.all()[-1].id
        prev_emp_num = len(Employees.query.all())
        response = tester.get(f'/employees/{id}/del', follow_redirects=True)
        new_emp_num = len(Employees.query.all())
        self.assertFalse(prev_emp_num == new_emp_num)

if __name__ == '__main__':
    unittest.main()
