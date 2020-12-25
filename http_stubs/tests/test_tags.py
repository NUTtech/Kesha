import pytest
from django.contrib.admin.helpers import Fieldset
from django.contrib.admin.sites import AdminSite
from django.http.request import HttpRequest

from http_stubs.admin import HTTPStubAdmin
from http_stubs.models import HTTPStub
from http_stubs.templatetags import stub_tags


class TestStubTags:
    """Tests for custom tags and filters for Django templates."""

    @pytest.mark.parametrize(
        'relative_url, is_regex, expect', (
            ('/check/', True, 'http://127.0.0.1'),
            ('/check/', False, 'http://127.0.0.1/check/'),
            ('check', False, 'http://127.0.0.1/check'),
            (None, False, ''),
        ),
    )
    def test_absolute_url_tag(self, relative_url, is_regex, expect):
        """Check that the absolute url is correct.

        :param relative_url: a http-stub url
        :param is_regex: regex url flag
        :param expect: a expect absolute url
        """
        req = HttpRequest()
        req.META = {
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '80',
        }
        form = HTTPStubAdmin(
            HTTPStub, AdminSite,
        ).get_form(req)(initial={'regex_path': is_regex})
        fieldset = Fieldset(form)
        url = stub_tags.absolute_url({'request': req}, relative_url, fieldset)
        assert url == expect

    def test_headers_to_list_filter(self):
        """Check that the list of headers is returned."""
        headers = '{"Content-Length": "2", "Accept": "text/html"}'
        headers_list = stub_tags.headers_to_list(headers)
        assert headers_list == ['Content-Length: 2', 'Accept: text/html']

    def test_headers_to_list_filter_invalid(self):
        """Check that the list of headers is empty."""
        headers = 'invalid headers format'
        headers_list = stub_tags.headers_to_list(headers)
        assert not headers_list
