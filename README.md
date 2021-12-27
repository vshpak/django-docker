# Django-проект "Архив книг и журналов"

## Руководство по запуску проекта:

1. Загрузить проект локально и в корне проекта выполнить команду docker-compose up

2. Перейти по пути http://127.0.0.1:8000/admin/ и проверить добавление и редактирование сущностей: издательства, книги, журналы, статьи

3. Проверить на работоспособность слеующие эндпоинты:
    - /pools/publishers/ (GET/POST)
    - /pools/publishers/{id} (GET/PUT/PATCH/DELETE)
    - /pools/journals/ (GET/POST)
    - /pools/journals/{id} (GET/PUT/PATCH/DELETE)
    - /pools/books/ (GET/POST)
    - /pools/books/{id} (GET/PUT/PATCH/DELETE)
    - /pools/journals/ (GET/POST)
    - /pools/journals/{id} (GET/PUT/PATCH/DELETE)
    - /store/journals/{id}/articles/ GET

4. Запустить выполнение интеграционных тестов командой pytest

5. Очистить созданные образ и контейнер:
```shell
docker rm django-docker_app_1
docker rmi django-docker_app:latest
```
