# Fitness Tracker

Веб-приложение для составления тренировок

___

+ [Установка локально](#title1)
+ [Структура проекта](#title2)
+ [Технологии](#title3)
+ [Контакты](#title4)
___

## <a id="title1"> **:computer: Установка локально**

### 1. Клонирование репозитория
```bash
git clone https://github.com/arssmol1029/fitness_tracker
cd fitness_tracker
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate #Linux/Mac
venv\Scripts\activate #Windows
pip install -r requirements.txt
```

### 3. Генерация ключа
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

### 4. Настройка окружения
Создайте файл .env в корне проекта на основе .env.example и заполните переменные:
```
SECRET_KEY=ваш-ключ-из-шага-3
DEBUG=False
```

### 5. Запуск миграций
```bash
python manage.py migrate
```

### 6. Создание суперпользователя (при необходимости)
```bash
python manage.py createsuperuser
```

### 7. Запуск сервера
```bash
python manage.py runserver
```

Сервер будет работать на http://127.0.0.1:8000

___

## <a id="title2"> :file_folder: Структура проекта

```text
fitness_tracker/  
├── fitness_tracker/            # Настройки, утилиты
│   ├── __pycache__ 
│   ├── __init__.py  
│   ├── asgi.py  
│   ├── settings.py             # Настройки Django  
│   ├── urls.py                 # Главные URL-адреса  
│   └── wsgi.py  
│  
├── static/                     # Статические файлы  
│   ├── css/  
│   └── js/  
│  
├── templates/                  # HTML шаблоны  
│   ├── base/
|   |   ├──404.html             # Страница ошибки
|   |   ├──base.html            # Базовый шаблон страницы (структура, шапка и тд)
|   |   └──profile.html         # Страница профиля
|   ├── registration/
|   └── tracker/                # Шаблоны страниц приложения
│  
├── tracker/                    # Приложение  
│   ├── __pycache__ 
│   ├── migrations/ 
│   ├── admin.py
│   ├── apps.py          
│   ├── forms.py                
│   ├── models.py
│   ├── serializers.py         # Сериализаторы (получение объекта в виде словаря)
│   ├── services.py            # Функции для views
│   ├── tests.py
│   ├── urls.py                # URL-адреса приложения
│   └── views.py 
│  
├── .env                        # Локальные переменные 
├── .gitignore                  # Игнорируемые файлы  
├── manage.py                   # Скрипт управления Django  
├── requirements.txt            # Зависимости 
└── README.md
```

## <a id="title3"> :shipit: Технологии

+ **Backend:** Python 3.12, Django 5.2, Django REST Framework
+ **Frontend:** HTML/CSS/JS, Bootstrap 5, JQuery
+ **Базы данных:** SQLite

## <a id="title4"> :mailbox_with_mail: Контакты

+ **Автор:** arssmol1029
+ **Telegram:** [@kepolb](https://t.me/kepolb)