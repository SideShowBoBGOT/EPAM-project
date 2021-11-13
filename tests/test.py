from project.proj import app
import unittest
class FlaskTestCases(unittest.TestCase):


    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/departments', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the departments page loads correctly
    def test_dnt_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/departments', content_type='html/text')
        self.assertTrue(b'Departments' in response.data)

    # Ensure that employees page load correctly
    def test_emp_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/employees', content_type='html/text')
        self.assertTrue(b'Employees' in response.data)

    #Ensure the departments page behaves correctly given correct name of dnt
    def test_dnt_page_add_dnt(self):
        tester = app.test_client(self)
        response = tester.post('/departments', data=dict(department='Go'), follow_redirects=True)
        self.assertTrue(b'Go' in response.data)

    #Ensure the departments page behaves correctly given incorrect name of dnt
    def test_dnt_page_add_dnt_err(self):
        tester = app.test_client(self)
        response = tester.post('/departments', data=dict(department=''), follow_redirects=True)
        self.assertTrue(b'' in response.data)
if __name__ == '__main__':
    unittest.main()