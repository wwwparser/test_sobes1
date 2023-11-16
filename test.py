import requests

base_url = 'http://127.0.0.1:5000'

# Тестовые данные
test_data = [
    {'field_email_1': '+7 123 456 78 90', 'field_phone_2': '12.12.2022'},
    {"name": "OrderForm", 'field_phone': '+7 987 654 32 10', 'field_date': '2022-12-12', 'field_email': 'example@example.com'},
    # {'field_email': '+7 111 222 33 44', 'field_phone': '01.01.2023', 'field_date': 'another@example.com'},
    # {'field_email': '+7 555 666 77 88', 'field_phone': '2023-01-01', 'field_date': 'name', 'field_text': 'city'},
    # {'field_email': '+7 999 888 77 66', 'field_phone': '2023-02-02', 'field_date': 'user@example.com', 'field_text': 'text'}
]

# Тестирование запросов
for data in test_data:
    response = requests.post(f'{base_url}/get_form', data=data)
    print(f"Request Data: {data}")
    print(f"Response: {response.text}")
    print("=" * 30)
