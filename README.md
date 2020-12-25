# Parrot
_Web-service for testing http requests and webhooks._

Project info:
[![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/umahighload/parrot-app/latest)](https://registry.hub.docker.com/r/umahighload/parrot-app)
![Python Version](https://img.shields.io/static/v1?label=python&message=3.8&color=blue)
![License](https://img.shields.io/static/v1?label=license&message=Apache+2&color=blue)

Build:
![autotests](https://github.com/Uma-Tech/parrot/workflows/autotests/badge.svg)
![build](https://github.com/Uma-Tech/parrot/workflows/build/badge.svg)

Code quality:
[![codecov](https://codecov.io/gh/Uma-Tech/parrot/branch/develop/graph/badge.svg)](https://codecov.io/gh/Uma-Tech/parrot)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Uma-Tech/parrot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Uma-Tech/parrot/context:python)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Uma-Tech_parrot&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=Uma-Tech_parrot)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Uma-Tech_parrot&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=Uma-Tech_parrot)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Uma-Tech_parrot&metric=security_rating)](https://sonarcloud.io/dashboard?id=Uma-Tech_parrot)

---

<p align="center">
    <img src="https://github.com/Uma-Tech/parrot/raw/master/static/parrot_icon.png">
</p>

## Links:
1. Repository: [https://github.com/Uma-Tech/parrot](https://github.com/Uma-Tech/parrot)
1. Documentation: [https://uma-tech.github.io/parrot/](https://uma-tech.github.io/parrot/)
1. Docker Hub: [https://registry.hub.docker.com/r/umahighload/parrot-app](https://registry.hub.docker.com/r/umahighload/parrot-app)
1. Issue tracker: [https://github.com/Uma-Tech/parrot/issues](https://github.com/Uma-Tech/parrot/issues)
1. Changelog: [https://github.com/Uma-Tech/parrot/blob/develop/CHANGELOG.md](https://github.com/Uma-Tech/parrot/blob/develop/CHANGELOG.md)

## Quickstart (with Docker)
1. Clone the repo
    ```shell
    git clone git@github.com:Uma-Tech/parrot.git
    ```

1. Build or download the docker image  
    _for build_
    ```shell
    make build
    ```
    _for download_
    ```shell script
    docker pull umahighload/parrot-app:latest
    ```

1. Apply migrations and create a superuser:
    ```shell
    make shell
    # inside the container
    python manage.py migrate  # apply migrations
    python manage.py createsuperuser  # create a superuser
    exit  ## leave from the container
    ```

1. Start app with required services
    ```shell
    make runserver
    ```

1. Service will be available at `http://127.0.0.1:8042/`

## Start the project for development without Docker
1. Clone the repo and go to the project directory
    ```shell
    git clone git@github.com:Uma-Tech/parrot.git
    cd parrot
    ```

1. Install dependencies
    ```shell
    poetry install
    ```

1. Start databases  
    _You can start databases in any other way_
   ```shell
    # start postgres
   docker run \
       --name postgres \
       -d \
       --rm \
       -e POSTGRES_PASSWORD=parrot \
       -e POSTGRES_USER=parrot \
       --network host \
       -v parrot_db:/var/lib/postgresql/data \
       postgres
   
    # start redis
   docker run \
       --name redis \
       -d \
       --rm \
       --network host \
       redis
    ```

1. Setting required environment variables  
   _Alternatively, you can create a local `.env` file with the variables_
    ```shell
    export PARROT_DB_HOST=127.0.0.1
    export PARROT_SECRET_KEY=NO_SECRET
    export PARROT_CELERY_BROKER_URL=redis://127.0.0.1
    ```

1. Build static
    ```shell
    poetry run python manage.py collectstatic --no-input
    ```

1. Apply database migrations
    ```shell
    poetry run python manage.py migrate
    ```

1. Create a django superuser
    ```shell
    poetry run python manage.py createsuperuser
    ```

1. Start the django app
    ```shell
    poetry run python manage.py runserver
    ```

1. Start the celery worker  
   _Run in a separate terminal window_
    ```shell
    poetry run celery -A parrot worker -l INFO -c 4
    ```
    

## System requirements
* docker ([https://www.docker.com/](https://www.docker.com/))
* docker-compose
    ([https://github.com/docker/compose](https://github.com/docker/compose))
* make
    ([https://www.gnu.org/software/make/](https://www.gnu.org/software/make/))
    _(all commands can be viewed by calling `make` without parameters)_
* poetry _(for development)_
  ([https://python-poetry.org/](https://python-poetry.org/))

## Components
1. Database postgres.
1. Database redis (for background celery-tasks).
1. Python-app based on Django Web Framework.

## Contributing
We welcome all contributions!  
See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute.  
You can start with [issues that need some help](https://github.com/Uma-Tech/parrot/issues)
right now.
