import requests

# URL вашего Django-приложения
url = 'http://localhost:8000/forms/get_form/'

# Данные, которые вы хотите отправить
data = {
    'f_name1': 'value1',
    'f_name2': 'value2'
}

# Отправка POST-запроса
response = requests.post(url, data=data)

# Печать ответа сервера
print(response.json(), 'response.json()')  # Печатает ответ сервера
