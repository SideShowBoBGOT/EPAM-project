import requests
BASE_URL = 'http://127.0.0.1:5000/'
data = {'func': 'del','id': 8, 'name': 'Bibop Rocksteady',
        'department': 'Python',
        'salary': '15000',
        'birth_date': '2020-01-01'}
response = requests.post(BASE_URL + 'api/admin/qwerty/employees', data=data )
print(response.json())