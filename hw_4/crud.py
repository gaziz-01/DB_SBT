import requests
from requests.auth import HTTPBasicAuth
import configparser
import json

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']

# URL кэша
url = 'https://localhost:11222/rest/v2/caches/contacts'

# Создание контактов
contacts = {
    "contact1": json.dumps({"first_name": "John", "last_name": "Doe", "phone": "1234567890", "address": "123 Elm St"}),
    "contact2": json.dumps({"first_name": "Jane", "last_name": "Doe", "phone": "0987654321", "address": "456 Oak St"})
}

# Добавление контактов в кэш
for key, value in contacts.items():
    put_response = requests.put(f"{url}/{key}", data=value, auth=HTTPBasicAuth(username, password), verify=False)
    print(f"Put response for {key}:", put_response.status_code)

# Чтение контактов из кэша
for key in contacts.keys():
    get_response = requests.get(f"{url}/{key}", auth=HTTPBasicAuth(username, password), verify=False)
    print(f"Get response for {key}:", get_response.text)

# Обновление контакта
updated_contact = json.dumps({"first_name": "John", "last_name": "Doe", "phone": "1122334455", "address": "789 Pine St"})
put_update_response = requests.put(f"{url}/contact1", data=updated_contact, auth=HTTPBasicAuth(username, password), verify=False)
print("Put response for contact1 update:", put_update_response.status_code)

# Проверка обновленного контакта
get_update_response = requests.get(f"{url}/contact1", auth=HTTPBasicAuth(username, password), verify=False)
print("Get response for updated contact1:", get_update_response.text)

# Удаление контакта
delete_response = requests.delete(f"{url}/contact2", auth=HTTPBasicAuth(username, password), verify=False)
print("Delete response for contact2:", delete_response.status_code)
