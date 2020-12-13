from django.http.request import HttpRequest

from http_stubs.templatetags import stub_tags


class TestStubTags:
    """Tests for custom tags and filters for Django templates."""

    def test_absolute_url_tag(self):
        """Check that the absolute url is returned."""
        req = HttpRequest()
        req.META = {
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '80',
        }
        relative_url = '/check/'
        url = stub_tags.get_absolute_url_tag({'request': req}, relative_url)
        assert url == 'http://127.0.0.1/check/'

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
