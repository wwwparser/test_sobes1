from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import datetime
import re

app = Flask(__name__)
db = TinyDB('forms_db.json')

# Пример тестовой базы данных
# initial_forms = [
#     {
#         "name": "MyForm",
#         "field_email_1": "email",
#         "field_phone_2": "phone"
#     },
#     {
#         "name": "OrderForm",
#         "field_email": "email",
#         "field_phone": "phone",
#         "field_date": "date"
#
#     }
# ]
#
# # Инициализация базы данных
# for form in initial_forms:
#     db.insert(form)


def validate_phone(phone):
    return re.match(r'^\+\d{1,3} \d{1,4} \d{1,4} \d{1,2} \d{1,2}$', phone) is not None

def validate_date(date):
    # Простая валидация даты в формате DD.MM.YYYY или YYYY-MM-DD
    date_formats = ['%d.%m.%Y', '%Y-%m-%d']
    for format in date_formats:
        try:
            datetime.datetime.strptime(date, format)
            return True
        except ValueError:
            pass
    return False


def validate_email(email):
    # Простая валидация email
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None


def guess_field_type(value):
    # Определить тип поля на основе правил валидации
    if validate_date(value):
        return "date"
    elif validate_phone(value):
        return "phone"
    elif validate_email(value):
        return "email"
    else:
        return "text"


def find_matching_form(form_data):
    for form in db:
        match = True
        for field_name, field_type in form.items():

            if field_name != "name" and field_name not in form_data:
                match = False
                break

            if field_name != "name" and (field_name not in form_data or guess_field_type(form_data[field_name]) != field_type):
                match = False
                break
        if match:
            return form["name"]
    return None

@app.route('/get_form', methods=['POST'])
def get_form():
    form_data = request.form.to_dict()
    matching_form = find_matching_form(form_data)

    if matching_form:
        return matching_form
    else:
        field_types = {field: guess_field_type(value) for field, value in form_data.items()}
        return jsonify(field_types)


if __name__ == '__main__':
    app.run(debug=True)
