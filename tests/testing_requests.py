import requests
BASE_URL = 'http://127.0.0.1:5000/'
data = {'login': 'admin', 'password': 'qwerty', 'from_date':'1970-01-01', 'to_date':'2021-01-01'}
response = requests.get(BASE_URL + f'api/employees/find?login=admin&password=qwerty&from_date=1970-01ghhgfhg-01&to_date=2021-01-01')
print(response.json())
