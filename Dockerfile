FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /articles

COPY poetry.lock pyproject.toml /articles/

RUN pip3 install poetry

RUN poetry install