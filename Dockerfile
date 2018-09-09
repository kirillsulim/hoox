FROM python:3.6-alpine

LABEL maintainer="kirillsulim@gmail.com"

RUN mkdir -p /app/src
COPY ./src /app/src
COPY ./setup.py /app
COPY ./README.md /app
COPY ./hoox.version /app

WORKDIR /app

RUN python setup.py install

ENTRYPOINT [ "hoox" ]
