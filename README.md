# Freeai API

## Overview

- Repository for Freeai API
- Using Flask

## Requirements

- [Docker](https://www.docker.com/)
- [Flask](https://a2c.bitbucket.io/flask/)

## Commands

```bash
# Create network
$ docker network create freeai_common_link

# Build docker image
$ docker-compose build

# Start servers
$ docker-compose up

# Migration
$ docker-compose exec freeai-api sh scripts/migrate.sh

# TODO Rollback
```


## Libraries

- [Flask](https://pypi.org/project/Flask/)

## Memo
