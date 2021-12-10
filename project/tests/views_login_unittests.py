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


if __name__ == '__main__':
    unittest.main()
