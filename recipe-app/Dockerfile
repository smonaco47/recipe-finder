# syntax=docker/dockerfile:1
FROM node:19-slim

WORKDIR /app
COPY . .
RUN npm install && cp -r /app/node_modules /tmp/node_modules
