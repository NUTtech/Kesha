FROM python:3.8

# Disables the buffer for instant output of messages to stdout from processes.
ENV PYTHONUNBUFFERED=1

# Install system requires
RUN apt-get update && \
    apt-get install -y libpq-dev wait-for-it && \
    apt-get clean

## Install poetry
RUN pip install --no-cache-dir poetry==1.0.9

WORKDIR /app/src

COPY pyproject.toml poetry.lock /app/src/

## Install app requires
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./ /app/src

# Build static
ARG PARROT_SECRET_KEY=no_secret
RUN /app/src/manage.py collectstatic --noinput

# Move scripts to /app
RUN find ./ -iname '*.sh' -exec mv '{}' /app/ \;
