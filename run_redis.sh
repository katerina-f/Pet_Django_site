#!/bin/bash

docker volume create --name=redis_custom_cian

docker-compose up -d --build
