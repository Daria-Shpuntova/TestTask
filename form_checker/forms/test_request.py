import os
import django
from django.test import TestCase, Client
from tinydb import TinyDB

# Установка переменной окружения для настроек
os.environ['DJANGO_SETTINGS_MODULE'] = 'form_checker.settings'
django.setup()

class TestGetFormView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Инициализация базы данных TinyDB и добавление шаблонов
        cls.db = TinyDB('db.json')
        cls.db.insert({'name': 'email_phone', 'fields': {'f_name1': 'email', 'f_name2': 'phone'}})
        cls.db.insert({'name': 'date_email_text', 'fields': {'f_name1': 'text', 'f_name2': 'date', 'f_name3': 'email'}})

    def setUp(self):
        self.client = Client()

    def test_valid_data(self):
        data = {
            'f_name1': 'example@example.com',
            'f_name2': '+7 123 456 78 90'
        }
        response = self.client.post('/forms/get_form/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('template_name', response.json())

    def test_invalid_data(self):
        data = {
            'f_name1': 'invalid_email',
            'f_name2': 'not_a_phone'
        }
        response = self.client.post('/forms/get_form/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Нет нужной формы', response.json())

    @classmethod
    def tearDownClass(cls):
        cls.db.truncate()  # Очищаем базу данных после тестов
        super().tearDownClass()


#import os
#import django
#from django.test import TestCase, Client
#
#
## Установка переменной окружения для настроек
#os.environ['DJANGO_SETTINGS_MODULE'] = 'form_checker.settings'
#django.setup()
#
#class TestGetFormView(TestCase):
#    def setUp(self):
#        self.client = Client()
#
#    def test_valid_data(self):
#        data = {
#            'f_name1': 'example@example.com',
#            'f_name2': '+7 123 456 78 90'
#        }
#        response = self.client.post('/forms/get_form/', data=data)
#        self.assertEqual(response.status_code, 200)
#        self.assertIn('template_name', response.json())
#
#    def test_invalid_data(self):
#        data = {
#            'f_name1': 'invalid_email',
#            'f_name2': 'not_a_phone'
#        }
#        response = self.client.post('/forms/get_form/', data=data)
#        self.assertEqual(response.status_code, 200)
#        self.assertIn('validation_results', response.json())