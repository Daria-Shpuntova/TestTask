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


