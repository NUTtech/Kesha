from typing import Callable

import pytest

from http_stubs.models import HTTPMethod, HTTPStub, LogEntry, ProxyHTTPStub


@pytest.fixture
def http_stub_factory() -> Callable[..., HTTPStub]:
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
def proxy_http_stub_factory() -> Callable[..., ProxyHTTPStub]:
    """Proxy HTTP stubs factory.

    :returns: factory closure
    """
    def factory(**kwargs) -> ProxyHTTPStub:
        """Create and return ProxyHTTPStub object.

        :param kwargs: model params
        :return: created stub
        """
        default_params = {
            'path': '/default_proxy_path/',
            'target_url': '',
            'method': HTTPMethod.GET.name,
            'target_method': HTTPMethod.GET.name,
        }
        default_params.update(kwargs)
        return ProxyHTTPStub.objects.create(**default_params)
    return factory


@pytest.fixture
def log_entity_factory(
    http_stub_factory,  # noqa: WPS442
) -> Callable[..., LogEntry]:
    """Log Entity factory.

    :param http_stub_factory: a factory for create a HttpStub
    :returns: factory closure
    """
    def factory(**kwargs) -> LogEntry:
        """Create and return LogEntry object.

        :param kwargs: model params
        :return: created stub
        """
        http_stub: HTTPStub = kwargs.get('http_stub') or http_stub_factory()
        default_params = {
            'path': http_stub.path,
            'method': http_stub.method,
            'source_ip': '127.0.0.1',
            'request_date': 1608757075,
            'request_body': '',
            'request_headers': {},
            'http_stub': http_stub,
            'result_script': '',
            'resp_status': 418,
        }
        default_params.update(kwargs)
        return LogEntry.objects.create(**default_params)
    return factory
