import pytest

from _pytest.fixtures import FixtureFunctionMarker


@pytest.fixture(autouse=True)
def db_connect(db: FixtureFunctionMarker):
    """Автоматическое подключение к базе для каждого теста.

    :param db: фикстура инициализирующая базу данных.
    """


# подключаем файлы фикстур
from http_stubs.tests.fixtures import *  # noqa
