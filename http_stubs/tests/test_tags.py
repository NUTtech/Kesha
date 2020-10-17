from django.http.request import HttpRequest

from http_stubs.templatetags.stub_tags import get_absolute_url_tag


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
        url = get_absolute_url_tag({'request': req}, relative_url)
        assert url == 'http://127.0.0.1/check/'
