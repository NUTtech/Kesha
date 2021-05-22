#!/usr/bin/env bash

wait-for-it "${KESHA_DB_HOST:-kesha-database}":5432 -s -t 180 \
&& python /app/src/manage.py migrate --noinput \
&& python /app/src/manage.py runserver 0.0.0.0:8042
