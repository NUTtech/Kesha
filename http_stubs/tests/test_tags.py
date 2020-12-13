from django.contrib.admin.helpers import Fieldset
from django.contrib.admin.sites import AdminSite
from django.http.request import HttpRequest

from http_stubs.admin import HTTPStubAdmin
from http_stubs.models import HTTPStub
from http_stubs.templatetags import stub_tags


class TestStubTags:
    """Tests for custom tags and filters for Django templates."""

    def test_absolute_url_tag_with_regex(self):
        """Check that the absolute url is correct if regex_path is true."""
        req = HttpRequest()
        req.META = {
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '80',
        }
        relative_url = '/check/'
        form = HTTPStubAdmin(
            HTTPStub, AdminSite,
        ).get_form(req)(initial={'regex_path': True})
        fieldset = Fieldset(form)
        url = stub_tags.absolute_url({'request': req}, relative_url, fieldset)
        assert url == 'http://127.0.0.1'

    def test_absolute_url_tag(self):
        """Check that the absolute url is returned."""
        req = HttpRequest()
        req.META = {
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '80',
        }
        relative_url = '/check/'
        form = HTTPStubAdmin(
            HTTPStub, AdminSite,
        ).get_form(req)(initial={'regex_path': False})
        fieldset = Fieldset(form)
        url = stub_tags.absolute_url({'request': req}, relative_url, fieldset)
        assert url == 'http://127.0.0.1/check/'

    def test_absolute_url_tag_without_slash(self):
        """Check that the absolute url is correct.

        When relative url doesn`t start with a slash.
        """
        req = HttpRequest()
        req.META = {
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '80',
        }
        relative_url = 'check'
        form = HTTPStubAdmin(
            HTTPStub, AdminSite,
        ).get_form(req)(initial={'regex_path': False})
        fieldset = Fieldset(form)
        url = stub_tags.absolute_url({'request': req}, relative_url, fieldset)
        assert url == 'http://127.0.0.1/check'

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
