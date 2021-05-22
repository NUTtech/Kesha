#!/usr/bin/env bash

wait-for-it "${KESHA_DB_HOST:-kesha-database}":5432 -s -t 180 \
&& pytest --cov
