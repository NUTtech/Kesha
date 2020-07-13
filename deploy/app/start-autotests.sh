#!/usr/bin/env bash

wait-for-it "${PARROT_DB_HOST:-parrot-database}":5432 -s -t 180 \
&& pytest --cov
