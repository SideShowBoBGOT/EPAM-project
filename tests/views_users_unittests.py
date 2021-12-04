import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join('..')))

from models.users import User
from wsgi import app

app.app_context().push()
ADMIN_LOGIN = User.query.get(1).login
ADMIN_PASSWORD = User.query.get(1).password


class FlaskTestCases(unittest.TestCase):
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
        login = User.query.all()[-1].login
        password = User.query.all()[-1].password
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


if __name__ == '__main__':
    unittest.main()
