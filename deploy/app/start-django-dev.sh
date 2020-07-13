#!/usr/bin/env bash

wait-for-it "${PARROT_DB_HOST:-parrot-database}":5432 -s -t 180 \
&& python /app/src/manage.py migrate --noinput \
&& python /app/src/manage.py runserver 0.0.0.0:8042
