# Приложение Financial_support_for_projects

API-приложение для сбора финансовой поддержки проектов. Пользователи могут просмотреть список всех проектов, включая необходимые и уже внесенные суммы. Зарегистрированные пользователи могут делать пожертвования и просматривать историю своих пожертвований.
Реализована возможность формирования отчёта в Google Sheet. В таблицу выгружаются данные закрытых проектов, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.


## Технологии
[![FastAPI](https://img.shields.io/badge/FastAPI-0.78.0-blue)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.9-blue?logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-blue)](https://docs.sqlalchemy.org/en/20/)
[![alembic](https://img.shields.io/badge/Alembic-1.7.7-blue)](https://alembic.sqlalchemy.org/en/latest/)
[![GoogleAPI](https://img.shields.io/badge/GoogleAPI-blue)](https://cloud.google.com/apis/docs/overview)
[![Pydantic](https://img.shields.io/badge/Pydantic-blue)](https://docs.pydantic.dev/latest/)
[![Asyncio](https://img.shields.io/badge/Asyncio-blue)](https://docs.python.org/3/library/asyncio.html)

Клонировать репозиторий в командной строке:

```
git clone git@github.com:Tatiana314/Financial_support_for_projects.git && sd Financial_support_for_projects
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
Linux/macOS: source env/bin/activate
windows: source env/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
В директории Financial_support_for_projects создать и заполнить файл .env:
```
touch .env

DATABASE_URI=<sqlite:///db.sqlite3>
SECRET_KEY=<SECRET_KEY>
FIRST_SUPERUSER_EMAIL = <EMAIL>
FIRST_SUPERUSER_PASSWORD=<PASSWORD>

# Доступ к сервисному аккаунту:
EMAIL = <EMAIL>
TYPE = <TYPE>
PROJECT_ID = "careful-ensign-413405"
PRIVATE_KEY_ID = "fc57537054c5264263b29862562ba3c3f0845528"
PRIVATE_KEY = <KEY>
CLIENT_EMAIL = <CLIENT_EMAIL>
CLIENT_ID = <CLIENT_ID>
AUTH_URI = <AUTH_URI>
TOKEN_URI = <TOKEN_URI>
AUTH_PROVIDER_X509_CERT_URL = <AUTH_PROVIDER_X509_CERT_URL>
CLIENT_X509_CERT_URL = <CLIENT_X509_CERT_URL>
```
Выполнить миграции:
```
alembic upgrade head
```
Запустить проект:
```
uvicorn app.main:app --reload 
```

Документация сервера:


* Формат документации — Swagger:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* Формат документации — ReDoc:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


## Автор
[Мусатова Татьяна](https://github.com/Tatiana314)
