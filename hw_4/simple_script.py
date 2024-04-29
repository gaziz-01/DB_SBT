import requests
from requests.auth import HTTPBasicAuth
import configparser

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']

# URL кэша
url = 'https://localhost:11222/rest/v2/caches/newest_cache'

# Добавление элемента в кэш
put_response = requests.put(f"{url}/example-key", data='example-value', auth=HTTPBasicAuth(username, password), verify=False)
print("Put response:", put_response.status_code)

# Получение элемента из кэша
get_response = requests.get(f"{url}/example-key", auth=HTTPBasicAuth(username, password), verify=False)
print("Get response:", get_response.text)

# Индексация и поиск
search_query = '{"query":"FROM newest_cache WHERE key=\'example-key\'"}'
query_url = f"{url}/search"
search_response = requests.post(query_url, data=search_query, auth=HTTPBasicAuth(username, password), verify=False)
print("Search response:", search_response.text)

# Удаление элемента из кэша
delete_response = requests.delete(f"{url}/example-key", auth=HTTPBasicAuth(username, password), verify=False)
print("Delete response:", delete_response.status_code)

