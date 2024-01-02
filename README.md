# API-сервис
## Описание
API-сервис собирает отзывы пользователей на произведения. Сами произведения в API не хранятся, 
здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:DEADRINO/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Посмотреть документацию можно по адресу:
```
http://127.0.0.1:8000/redoc/
```



## Стек технологий
Django, DRF, Django ORM, Notion, GitHub, HTML, CSS, React.
