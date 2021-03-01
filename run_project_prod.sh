#!/bin/bash

docker volume create --name=redis_custom_cian
docker volume create --name=postgres_custom_cian

docker-compose -f docker-compose.prod.yml up -d --build
