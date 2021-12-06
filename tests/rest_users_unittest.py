import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from models.users import User
from wsgi import app

import unittest

app.app_context().push()
ADMIN_LOGIN = User.query.get(1).login
ADMIN_PASSWORD = User.query.get(1).password


class FlaskTestCases(unittest.TestCase):
    # Ensure server responds correctly to user get API request
    def test_user_api_get(self):
        tester = app.test_client(self)
        response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                              follow_redirects=True)
        self.assertTrue(User.query.all()[-1].login.encode() in response.data)

    # Ensure server responds correctly to user add API request given correct args
    def test_user_api_add(self):
        tester = app.test_client(self)
        new_login = 'sdlkfnkslodnfalfnalfnakfoeipwneworf'
        new_password = 'dsjkfnoq302032refnmpdospmpksd'
        response = tester.get(f'/api/users/add?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}'
                              f'&new_login={new_login}&new_password={new_password}',
                              follow_redirects=True)
        response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                              follow_redirects=True)
        self.assertTrue(new_login.encode() in response.data)
        id = User.query.all()[-1].id
        response = tester.get(f'/api/users/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)

    # Ensure server responds correctly to user add API request given incorrect args
    def test_user_add_err(self):
        tester = app.test_client(self)
        login_vars = ('', 'incorrect', User.query.all()[0].login)
        password_vars = ('', 'incorrect', User.query.all()[0].password)
        new_login_vars = ('', 'login')
        new_password_vars = ('', 'password')
        variations = []
        for login in login_vars:
            for password in password_vars:
                for new_login in new_login_vars:
                    for new_password in new_password_vars:
                        variations.append((login, password, new_login, new_password))
        for variation in variations[:-1]:
            prev_users = User.query.all()
            response = tester.get(f'/api/users/add?login={variation[0]}&password={variation[1]}'
                                  f'&new_login={variation[2]}&new_password={variation[3]}',
                                  follow_redirects=True)
            new_users = User.query.all()

            self.assertTrue(prev_users == new_users)

    # Ensure server responds correctly to user edit API request given correct args
    def test_user_api_edit(self):
        tester = app.test_client(self)
        login = 'sdlkfnkslodnfalfnalfndsfakfoeipwn eworf'
        password = 'dsjkfnoq-302-032refsdfsdnmpdos[pmpksd'
        response = tester.get(f'/api/users/add?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}'
                              f'&new_login={login}&new_password={password}',
                              follow_redirects=True)
        new_login = 'sdawqmvm]dc sdzzzzzqqq'
        new_password = 'dsvmmm2130opo2nds....'
        id = User.query.all()[-1].id
        response = tester.get(f'/api/users/edit?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}'
                              f'&new_login={new_login}&new_password={new_password}&id={id}',
                              follow_redirects=True)
        response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                              follow_redirects=True)
        self.assertTrue(new_login.encode() in response.data)
        response = tester.get(f'/api/users/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)

    # Ensure server responds correctly to user edit API request given incorrect args
    def test_user_api_edit_err(self):
        tester = app.test_client(self)
        login = 'sdlkfnkslodnfalfnalfndsfakfoeipwn eworf'
        password = 'dsjkfnoq-302-032refsdfsdnmpdos[pmpksd'
        response = tester.get(f'/api/users/add?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}'
                              f'&new_login={login}&new_password={password}',
                              follow_redirects=True)
        old_response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        login_vars = ('', 'incorrect', User.query.all()[0].login)
        password_vars = ('', 'incorrect', User.query.all()[0].password)
        new_login_vars = ('', 'login')
        new_password_vars = ('', 'password')
        id_vars = ('', '3s', -1, User.query.all()[-1].id)
        variations = []
        for login in login_vars:
            for password in password_vars:
                for new_login in new_login_vars:
                    for new_password in new_password_vars:
                        for id in id_vars:
                            variations.append((login, password, new_login, new_password, id))
        for variation in variations[:-1]:
            response = tester.get(f'/api/users/edit?login={variation[0]}&password={variation[1]}'
                                  f'&new_login={variation[2]}&new_password={variation[3]}&id={variation[4]}',
                                  follow_redirects=True)
            new_response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                      follow_redirects=True)
            self.assertTrue(old_response.data == new_response.data)
        id = User.query.all()[-1].id
        response = tester.get(f'/api/users/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)

    # Ensure server responds correctly to user del API request given correct args
    def test_users_api_del(self):
        tester = app.test_client(self)
        old_response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        login = 'sdlkfnkslodnfalfnalfndseworf'
        password = 'dsjkfnoqpmpksd'
        response = tester.get(f'/api/users/add?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}'
                              f'&new_login={login}&new_password={password}',
                              follow_redirects=True)
        id = User.query.all()[-1].id
        response = tester.get(f'/api/users/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                              follow_redirects=True)
        new_response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        self.assertTrue(old_response.data == new_response.data)

    # Ensure server responds correctly to user del API request given incorrect args
    def test_users_api_del_err(self):
        tester = app.test_client(self)
        old_response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                  follow_redirects=True)
        id_vars = ('', '3s', -1)
        for id in id_vars:
            response = tester.get(f'/api/users/del?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}&id={id}',
                                  follow_redirects=True)
            new_response = tester.get(f'/api/users/get?login={ADMIN_LOGIN}&password={ADMIN_PASSWORD}',
                                      follow_redirects=True)
            self.assertTrue(old_response.data == new_response.data)


if __name__ == '__main__':
    unittest.main()
