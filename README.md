# Приложение QRkot_spreadseets

Приложение для Благотворительного фонда поддержки котиков QRKot. 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
Реализована возможность формирования отчёта в гугл-таблице. В таблицу выгружаются данные закрытых проектов, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.


## Технологии
- Python 3.9
- FastAPI 0.78.0
- SQLAlchemy 1.4
- Alembic 1.7.7
- Google API

Клонировать репозиторий в командной строке:

```
git clone git@github.com:Tatiana314/QRkot_spreadsheets.git
```
Перейти в директорию:

```
mkdir QRkot_spreadsheets
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл настроек окружения:

```
touch .env
```

Заполнить его:

```
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

Запустить:

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
