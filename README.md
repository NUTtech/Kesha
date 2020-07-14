# Parrot
_Web-service for testing http-requests and webhooks._

[![codecov](https://codecov.io/gh/Uma-Tech/parrot/branch/develop/graph/badge.svg)](https://codecov.io/gh/Uma-Tech/parrot)
![autotests](https://github.com/Uma-Tech/parrot/workflows/autotests/badge.svg)
[![Python Version](https://img.shields.io/static/v1?label=python&message=3.8&color=blue)]()
[![License](https://img.shields.io/static/v1?label=license&message=Apache+2&color=blue)]()

---

<p align="center">
    <img src="https://github.com/Uma-Tech/parrot/raw/master/static/parrot_icon.png">
</p>

## Quickstart
1. Clone the repo
    ```shell script
    git clone git@github.com:Uma-Tech/parrot.git
    ```

1. Build
    ```shell script
    make build
    ```

1. Apply migrations and create a superuser:
    ```shell script
    make shell
    # inside the container
    python manage.py migrate  # apply migrations
    python manage.py createsuperuser  # create a superuser
    exit  ## leave from the container
    ```

1. Start app with required services
    ```shell script
    make runserver
    ```

1. Service will be available at `http://127.0.0.1:8042/`

## System requires
* docker ([https://www.docker.com/](https://www.docker.com/))
* docker-compose
    ([https://github.com/docker/compose](https://github.com/docker/compose))
* make
    ([https://www.gnu.org/software/make/](https://www.gnu.org/software/make/))
    _(all commands can be viewed by calling `make` without parameters)_

## Components
1. Database postgres.
1. Python-app based on Django Web Framework.

## Contributing
We welcome all contributions!  
See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute.  
You can start with [issues that need some help](https://github.com/Uma-Tech/parrot/issues)
right now.

