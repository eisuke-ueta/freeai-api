#!/usr/bin/env bash

until mysql -h ${MYSQL_HOST} -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -e "show databases"; do
    >&2 echo "mysql is unavailable - sleeping"
    sleep 1
done

python3 main.py