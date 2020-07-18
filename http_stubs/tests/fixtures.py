from typing import Callable

import pytest

from http_stubs.models import HTTPMethod, HTTPStub


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
