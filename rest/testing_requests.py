import requests
BASE_URL = 'http://127.0.0.1:5000/'
data = {'func': 'add', 'department': 'Fortran'}
response = requests.get(BASE_URL + 'api/admin/qwerty/departments', data=data)
print(response.json())