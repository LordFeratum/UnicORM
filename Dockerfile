FROM python:3.6-alpine
WORKDIR /opt

ENV PYTHONPATH=/opt/
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk --no-cache add \
      ca-certificates \
      openssl-dev \
      libffi-dev \
      libc-dev \
      gcc

COPY . /opt/
RUN pip install -r /opt/requirements-test.txt
