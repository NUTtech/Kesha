#!/usr/bin/env bash

wait-for-it "${KESHA_DB_HOST:-kesha-database}":5432 -s -t 180 \
&& python /app/src/manage.py migrate --noinput \
&& uvicorn kesha.asgi:application --host '0.0.0.0' --port 8042
