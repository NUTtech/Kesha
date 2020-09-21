# Local run

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
