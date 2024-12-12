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
print(response.text)
print(response.json(), 'response.json()')  # Печатает ответ сервера
print(response, 'response')
print(response.text)

#import requests
#
## URL вашего Django-приложения для получения CSRF-токена
#get_csrf_url = 'http://localhost:8000/'
#
## Получаем CSRF-токен
#session = requests.Session()
#response = session.get(get_csrf_url)
#
## Извлекаем CSRF-токен из cookies
#csrf_token = session.cookies['csrftoken']
#
## URL для отправки POST-запроса
#url = 'http://localhost:8000/forms/get_form/'
#
## Данные, которые вы хотите отправить
#data = {
#    'f_name1': 'value1',
#    'f_name2': 'value2',
#    'csrfmiddlewaretoken': csrf_token  # Добавляем CSRF-токен
#}
#
## Отправка POST-запроса с CSRF-токеном
#response = session.post(url, data=data)
#
## Печать ответа сервера
#print(response.text)  # Печатает ответ сервера
