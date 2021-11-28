import requests
BASE_URL = 'http://127.0.0.1:5000/'
data = {'func': 'find', 'From': '2020-01-11', 'To': '1994-10-11' }
response = requests.post(BASE_URL + 'api/admin/qwerty/employees', data=data )
print(response.json())