# syntax=docker/dockerfile:1
FROM python:3.9-slim

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends "openjdk-17-jre-headless" ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=/usr/local/spark
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
    PATH="${PATH}:${SPARK_HOME}/bin"

WORKDIR /src

RUN pip install poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install

COPY . .