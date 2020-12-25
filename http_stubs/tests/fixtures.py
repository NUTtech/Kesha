from typing import Callable

import pytest

from http_stubs.models import HTTPMethod, HTTPStub, LogEntry


@pytest.fixture
def http_stub_factory() -> Callable:
    """HTTP stubs factory.

    :returns: factory closure
    """
    def factory(**kwargs) -> HTTPStub:
        """Create and return HTTPStub object.

        :param kwargs: model params
        :return: created stub
        """
        default_params = {
            'path': '/default_path/',
            'method': HTTPMethod.GET.name,
        }
        default_params.update(kwargs)
        return HTTPStub.objects.create(**default_params)
    return factory


@pytest.fixture
def log_entity_factory(http_stub_factory) -> Callable:  # noqa: WPS442
    """Log Entity factory.

    :param http_stub_factory: a factory for create a HttpStub
    :returns: factory closure
    """
    def factory(**kwargs) -> LogEntry:
        """Create and return HTTPStub object.

        :param kwargs: model params
        :return: created stub
        """
        http_stub: HTTPStub = kwargs.get('http_stub') or http_stub_factory(
            path='/default_path/',
            method=HTTPMethod.GET.name,
        )
        default_params = {
            'path': http_stub.path,
            'method': http_stub.method,
            'source_ip': '127.0.0.1',
            'date': 1608757075,
            'body': '',
            'headers': {},
            'http_stub': http_stub,
            'result_script': '',
        }
        default_params.update(kwargs)
        return LogEntry.objects.create(**default_params)
    return factory
