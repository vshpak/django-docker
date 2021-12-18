FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml /usr/src/app/

RUN pip install --upgrade pip  \
 && pip install poetry \
 && poetry install \
 && pytest