from typing import Callable

import pytest

from http_stubs.models import HTTPMethod, HTTPStub


@pytest.fixture
def http_stub_factory() -> Callable:
    """Фабрика для создания объектов HTTPStub.

    :returns: фвбрика-замыкание
    """
    def factory(**kwargs) -> HTTPStub:
        """Создать и вернуть объект HTTPStub.

        :param kwargs: параметры для модели
        :return: созданная заглушка
        """
        default_params = {
            'path': '/default_path/',
            'method': HTTPMethod.GET.name,
        }
        default_params.update(kwargs)
        return HTTPStub.objects.create(**default_params)
    return factory
