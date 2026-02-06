# Fitness Tracker

Веб-приложение для планирования и отслеживания тренировочного процесса.

## Функциональность

В проекте реализованы связанные модули:

- **Календарь тренировок** — планирование тренировок по датам и контроль выполнения.
- **Мои шаблоны** — создание и хранение шаблонов тренировок для повторного использования.
- **Библиотека упражнений** — каталог упражнений для составления тренировочных планов.

## Запуск в Docker

### Требования
- Docker
- Docker Compose

### Быстрый старт
```bash
cp .env.example .env
docker compose up --build
```

Приложение будет доступно по адресу:  
http://localhost:8000

## Администрирование

Админ-панель:  
http://localhost:8000/admin/

Создание суперпользователя:
```bash
docker compose exec web python manage.py createsuperuser
```

## Полезные команды

Остановить контейнеры:
```bash
docker compose down
```

Остановить и удалить данные SQLite (volume):
```bash
docker compose down -v
```

Выполнить миграции вручную:
```bash
docker compose exec web python manage.py migrate
```

## Переменные окружения (.env)

Минимально рекомендуется задать:

- `SECRET_KEY` — секретный ключ Django
- `DEBUG` — `1/0` или `true/false`
- `ALLOWED_HOSTS` — список хостов через запятую
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — параметры базы данных (значения по умолчанию есть в `.env.example`)

## Технологии

+ **Backend:** Python 3.12, Django 5.2
+ **Frontend:** HTML/CSS/JS, Bootstrap 5, JQuery
+ **Базы данных:** PostgreSQL

## Контакты

+ **Автор:** arssmol1029
+ **Telegram:** [@kepolb](https://t.me/kepolb)