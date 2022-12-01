# syntax=docker/dockerfile:1
FROM python:3.9-slim

WORKDIR /src

RUN pip install poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install

COPY . .