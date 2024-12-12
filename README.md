Тестовое задание Python Junior + для е.Ком
Web-приложение для определения заполненных форм.


Проект на Django
Разработка была сделана в Pycharm


Команда для получения по урлу /forms/get_form/ POST-запроса с данными f_name1=value1&f_name2=value2

Команда выполняется из консоли, без использования PowerShell
TestTask\form_checker>curl -X POST -d "f_name1=value1&f_name2=value2" http://localhost:8000/forms/get_form/


Проведение тестов:
TestTask\form_checker>  python manage.py test forms.test_request



Стек:

Python 3.12
Django 5.1.4
tinyDB



