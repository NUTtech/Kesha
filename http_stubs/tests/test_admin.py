import pytest
from django.http import HttpRequest

from http_stubs.admin import (
    HTTPStubAdminBase,
    LogEntryAdminBase,
    ProxyLogEntryAdmin,
)
from http_stubs.models import HTTPStub, LogEntry, ProxyLogEntity


class TestLogEntryAdminBase:
    """Tests for LogEntryAdminBase class."""

    instance = LogEntryAdminBase(LogEntry, '')

    def test_has_add_permission(self):
        """Should always return false."""
        assert self.instance.has_add_permission() is False

    @pytest.mark.parametrize(
        'string, expect', (
            ('', ''),
            ('bad json', ''),
            ('{"not":"indented"}', '{\n  "not": "indented"\n}'),
            ('{\n  "indent": "json"\n}', '{\n  "indent": "json"\n}'),
        ),
    )
    def test_pretty_str(self, string, expect):
        """Test pretty_str method."""
        assert self.instance.pretty_str(string) == expect

    def test_pretty_request_body(self):
        """Test pretty_request_body method."""
        mock = type('mock', (), {'request_body': '{"valid":"json"}'})
        expect = '{\n  "valid": "json"\n}'
        assert self.instance.pretty_request_body(mock) == expect


class TestProxyLogEntryAdmin:
    """Tests for ProxyLogEntryAdmin class."""

    instance = ProxyLogEntryAdmin(ProxyLogEntity, '')

    def test_pretty_response_body(self):
        """Test for pretty_response_body method."""
        mock = type('mock', (), {'response_body': '{"valid":"json"}'})
        expect = '{\n  "valid": "json"\n}'
        assert self.instance.pretty_response_body(mock) == expect


class TestHTTPStubAdminBase:
    """Tests for HTTPStubAdminBase class."""

    instance = HTTPStubAdminBase(HTTPStub, '')

    def test_enable_action(self, http_stub_factory):
        """Test for enable_action method."""
        stub = http_stub_factory(is_active=False)
        self.instance.enable_action(HttpRequest(), HTTPStub.objects.all())
        stub.refresh_from_db()

        assert stub.is_active is True

    def test_disable_action(self, http_stub_factory):
        """Test for disable_action method."""
        stub = http_stub_factory(is_active=True)
        self.instance.disable_action(HttpRequest(), HTTPStub.objects.all())
        stub.refresh_from_db()

        assert stub.is_active is False
