version: "3"

services:
  app:
    env_file:
      - .env
    command:
        - /bin/bash
        - -c
        - |
          poetry run python manage.py migrate
          poetry run python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
          poetry run python manage.py runserver 0.0.0.0:8000
    build: .
    volumes:
      - .:/usr/src/app
    ports:
      - "8000:8000"