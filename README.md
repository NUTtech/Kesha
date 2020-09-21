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

## Quickstart
1. Clone the repo
    ```shell script
    git clone git@github.com:Uma-Tech/parrot.git
    ```

1. Build or download the docker image  
    _for build_
    ```shell script
    make build
    ```
    _for download_
    ```shell script
    docker pull umahighload/parrot-app:latest
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

