import requests
import re
BASE_URL = 'http://127.0.0.1:5000/'
data = {'login': 'admin', 'password': 'qwerty', 'id': 1, 'new_department': 'F#'}
response = requests.post(BASE_URL + 'api/departments/get', data=data)
print(response.json())
