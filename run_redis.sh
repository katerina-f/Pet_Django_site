#!/bin/bash

docker volume create --name=redis

docker-compose up -d --build
