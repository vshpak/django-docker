FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/articles

COPY poetry.lock pyproject.toml /usr/src/articles/

RUN pip install --upgrade pip  \
 && pip install poetry \
 && poetry install