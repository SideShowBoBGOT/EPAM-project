import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join('..')))

from models.departments import Departments
from models.users import User
from wsgi import app

app.app_context().push()
ADMIN_LOGIN = User.query.get(1).login
ADMIN_PASSWORD = User.query.get(1).password


class FlaskTestCases(unittest.TestCase):
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
        # set previous name of department
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


if __name__ == '__main__':
    unittest.main()
