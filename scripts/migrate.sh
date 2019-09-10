#!/usr/bin/env bash

mysql -h ${MYSQL_HOST} -u ${MYSQL_USER} -p${MYSQL_PASSWORD} --database=freeai -e "source mysql/deploy_schemas.sql"

# TODO Refresh database