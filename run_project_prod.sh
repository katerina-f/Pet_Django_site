#!/bin/bash

docker volume create --name=redis_custom_cian
docker volume create --name=postgres_custom_cian
docker volume create --name=static_volume

docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up --build
