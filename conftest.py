import pytest

from _pytest.fixtures import FixtureFunctionMarker

from parrot import celery_app

celery_app.conf['CELERY_ALWAYS_EAGER'] = True


@pytest.fixture(autouse=True)
def db_connect(db: FixtureFunctionMarker):
    """Automatically runs on database connection for every test.

    :param db: fixture for the database initialization
    """


# Adds fixtures
from http_stubs.tests.fixtures import *  # noqa
