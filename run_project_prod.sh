#!/bin/bash

docker volume create --name=redis_custom_cian
docker volume create --name=postgres_custom_cian

docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py wait_for_db
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata *.json
