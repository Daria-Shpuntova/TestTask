from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from tinydb import TinyDB, Query
import re

# Инициализация базы данных TinyDB
db = TinyDB('db.json')

def value_name(value):
    if re.match(r'^\d{2}\.\d{2}\.\d{4}$', value) or re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return 'date'
    elif re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return 'phone'
    elif re.match(r'^[\w\.-]+@[\w\.-]+$', value):
        return 'email'
    else:
        return 'text'

class GetFormView(View):
    @csrf_exempt
    def post(self, request):
        # Получаем данные из POST-запроса
        form_data = request.POST
        # Словарь для хранения типов полей и их валидации
        validation_results = {}

        # Определяем типы для каждого поля и проверяем их на валидацию
        for key, value in form_data.items():
            field_type = value_name(value)
            validation_results[key] = field_type

        # Извлекаем шаблоны из базы данных
        templates = db.all()  # Получаем все записи из базы данных

        # Проверка на подходящий шаблон
        for template in templates:
            template_name = template['name']
            template_fields = template['fields']

            # Проверяем, все ли поля шаблона присутствуют в форме
            if all(field in form_data for field in template_fields):
                # Проверяем, соответствуют ли типы полей
                if all(validation_results[field] == template_fields[field] for field in template_fields):
                    # Если все поля совпадают по типу, возвращаем имя шаблона
                    return JsonResponse({'template_name': template_name})

        # Если подходящий шаблон не найден, возвращаем результаты валидации
        return JsonResponse({'validation_results': validation_results})



#from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#import json
#import re
#from .models import FormTemplate
#
#from django.views import View


#class GetFormView(View):
#    @csrf_exempt  # Отключаем CSRF для тестирования, но не рекомендуется на продакшене
#    def post(self, request):
#        # Получаем данные из POST-запроса
#        data = request.POST
#
#        # Здесь вы будете обрабатывать логику валидации
#        field_types = self.validate_fields(data)
#
#        # Здесь вы можете проверить, совпадают ли поля с известными шаблонами
#        template_name = self.find_matching_template(data)
#
#        if template_name:
#            return JsonResponse({'template_name': template_name})
#        else:
#            return JsonResponse(field_types)
#
#    def validate_fields(self, data):
#        field_types = {}
#        for field_name, value in data.items():
#            if self.is_valid_date(value):
#                field_types[field_name] = 'date'
#            elif self.is_valid_phone(value):
#                field_types[field_name] = 'phone'
#            elif self.is_valid_email(value):
#                field_types[field_name] = 'email'
#            else:
#                field_types[field_name] = 'text'
#        return field_types
#
#    def is_valid_date(self, value):
#        # Проверка на валидный формат даты
#        date_patterns = [r'^\d{2}\.\d{2}\.\d{4}$', r'^\d{4}-\d{2}-\d{2}$']
#        return any(re.match(pattern, value) for pattern in date_patterns)
#
#    def is_valid_phone(self, value):
#        # Проверка на валидный формат телефона
#        phone_pattern = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
#        return re.match(phone_pattern, value) is not None
#
#    def is_valid_email(self, value):
#        # Проверка на валидный формат email
#        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#        return re.match(email_pattern, value) is not None
#
#    def find_matching_template(self, data):
#        # Здесь вы должны реализовать логику поиска подходящего шаблона
#        # Например, можно использовать заранее определенные шаблоны
#        templates = {
#            'MyForm': ['user_name', 'order_date', 'lead_email'],
#            'OrderForm': ['order_number', 'customer_phone', 'delivery_date'],
#        }
#
#        for template_name, required_fields in templates.items():
#            if all(field in data for field in required_fields):
#                return template_name
#        return None
#
#TEMPLATES = {
#    'email_phone': {'f_name1': 'email', 'f_name2': 'phone'},
#    'date_email_text': {'f_name1': 'text', 'f_name2': 'date', 'f_name3': 'email'},
#}
#
#def value_name(value):
#    if (re.match(r'^\d{2}\.\d{2}\.\d{4}$', value)) or bool(re.match(r'^\d{4}-\d{2}-\d{2}$', value)):
#        return 'date'
#    elif re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
#        return 'phone'
#    elif re.match(r'^[\w\.-]+@[\w\.-]+$', value):
#        return 'email'
#    else:
#        return 'text'
#
#
#class GetFormView(View):
#    @csrf_exempt
#    def post(self, request):
#        # Получаем данные из POST-запроса
#        form_data = request.POST
#        # Словарь для хранения типов полей и их валидации
#        validation_results = {}
#
#        # Определяем типы для каждого поля и проверяем их на валидацию
#        for key, value in form_data.items():
#            field_type = value_name(value)
#            validation_results[key] = field_type
#
#        # Проверка на подходящий шаблон
#        for template_name, template_fields in TEMPLATES.items():
#            # Проверяем, все ли поля шаблона присутствуют в форме
#            if all(field in form_data for field in template_fields):
#                # Проверяем, соответствуют ли типы полей
#                if all(validation_results[field] == template_fields[field] for field in template_fields):
#                    # Если все поля совпадают по типу, возвращаем имя шаблона
#                    return JsonResponse({'template_name': template_name})
#
#        # Если подходящий шаблон не найден, возвращаем результаты валидации
#        return JsonResponse({'Нет нужной формы': validation_results})
#
#@csrf_exempt
#def get_form(request):
#   if request.method == 'POST':
#       data = request.POST
#       form_fields = {key: value for key, value in data.items()}
#
#       # Получаем все шаблоны форм из базы данных
#       templates = FormTemplate.objects.all()
#       matching_template = None
#
#       for template in templates:
#           template_fields = template.fields
#           if all(field in form_fields and validate_field(field, form_fields[field]) for field in template_fields):
#               matching_template = template
#               break
#
#       if matching_template:
#           return JsonResponse({'template_name': matching_template.name})
#
#       # Если подходящего шаблона не найдено, возвращаем типы полей
#       field_types = {field: determine_field_type(field, form_fields[field]) for field in form_fields}
#       return JsonResponse(field_types)
#
#   return JsonResponse({'error': 'Invalid request method'}, status=400)

#def validate_field(field_name, value):
#   if field_name.startswith('date_'):
#       return bool(re.match(r'^\d{2}\.\d{2}\.\d{4}$', value)) or bool(re.match(r'^\d{4}-\d{2}-\d{2}$', value))
#   elif field_name.startswith('phone_'):
#       return bool(re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value))
#   elif field_name.startswith('email_'):
#       return bool(re.match(r'^[\w\.-]+@[\w\.-]+$', value))
#   return True  # Для текстовых полей
#
#def determine_field_type(field_name, value):
#   if field_name.startswith('date_'):
#       return 'date'
#   elif field_name.startswith('phone_'):
#       return 'phone'
#   elif field_name.startswith('email_'):
#      return 'email'
#   return 'text'
#
#