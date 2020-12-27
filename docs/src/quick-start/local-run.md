# Local run

## Quickstart (with Docker)
1. Clone the repo
    ```shell
    git clone git@github.com:Uma-Tech/parrot.git
    cd parrot
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

1. Start the app and its dependencies
    ```shell
    make runserver
    ```

1. You will be able to access the service at `http://127.0.0.1:8042/`

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
    ```shell
    export PARROT_DB_HOST=127.0.0.1
    export PARROT_SECRET_KEY=NO_SECRET
    export PARROT_CELERY_BROKER_URL=redis://127.0.0.1
    ```
   _Alternatively, you can create a local `.env` file with the variables_

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
