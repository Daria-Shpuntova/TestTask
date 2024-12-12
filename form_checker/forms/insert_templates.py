from tinydb import TinyDB

# Инициализация базы данных TinyDB
db = TinyDB('db.json')

# Функция для добавления шаблонов форм
def add_form_templates():
    # Пример добавления шаблонов форм
    db.insert({'name': 'email_phone', 'fields': {'f_name1': 'email', 'f_name2': 'phone'}})
    db.insert({'name': 'date_email_text', 'fields': {'f_name1': 'text', 'f_name2': 'date', 'f_name3': 'email'}})

    print("Шаблоны форм успешно добавлены в базу данных.")

if __name__ == "__main__":
    add_form_templates()
