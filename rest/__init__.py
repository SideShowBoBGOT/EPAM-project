from flask_restful import Api
from .rest_users import UserAPIget, UserAPIadd, UserAPIedit, UserAPIdel
from .rest_departments import DepartmentsAPIget, DepartmentsAPIadd, DepartmentsAPIedit, DepartmentsAPIdel
from .rest_employees import  EmployeesAPIget, EmployeesAPIadd, EmployeesAPIfind, EmployeesAPIedit, EmployeesAPIdel

r_api = Api()

r_api.add_resource(UserAPIget, '/api/users/get')
r_api.add_resource(UserAPIadd, '/api/users/add')
r_api.add_resource(UserAPIedit, '/api/users/edit')
r_api.add_resource(UserAPIdel, '/api/users/del')

r_api.add_resource(DepartmentsAPIget, '/api/departments/get')
r_api.add_resource(DepartmentsAPIadd, '/api/departments/add')
r_api.add_resource(DepartmentsAPIedit, '/api/departments/edit')
r_api.add_resource(DepartmentsAPIdel, '/api/departments/del')

r_api.add_resource(EmployeesAPIget, '/api/employees/get')
r_api.add_resource(EmployeesAPIadd, '/api/employees/add')
r_api.add_resource(EmployeesAPIfind, '/api/employees/find')
r_api.add_resource(EmployeesAPIedit, '/api/employees/edit')
r_api.add_resource(EmployeesAPIdel, '/api/employees/del')








