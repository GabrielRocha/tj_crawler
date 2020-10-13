FROM python:3.8-alpine as base

WORKDIR  /opt/code

ADD requirements.txt /opt/code

RUN apk add --update --no-cache \
    g++ \
    gcc \
    libxslt-dev \
    libxml2-dev

FROM base as dev

RUN pip install -r requirements.txt