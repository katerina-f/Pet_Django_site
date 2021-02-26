#!/bin/bash

docker volume create --name=redis_custom_cian
docker volume create --name=app_custom_cian
docker volume create --name=postgres_custom_cian

docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
