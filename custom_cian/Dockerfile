
FROM python:3.8.3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libressl-dev libffi-dev
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /usr/src/custom_cian
COPY . /usr/src/custom_cian
WORKDIR /usr/src/custom_cian
