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

COPY requirements*.txt /opt/

ARG INCLUDE_TEST=0
RUN REQUERIMENTS_FILE="requirements.txt"; \
    if [ $INCLUDE_TEST == 1 ]; then \
        REQUERIMENTS_FILE="requirements-test.txt"; \
    fi; \
    pip install -r /opt/$REQUERIMENTS_FILE
