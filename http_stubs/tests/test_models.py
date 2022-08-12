from http_stubs.models import HTTPStub, LogEntry


class TestAbstractHTTPStub:
    """Tests for AbstractHTTPStub class through HTTPStub."""

    model = HTTPStub(
        method='test_method',
        path='test_path',
    )

    def test_str(self):
        """Test magic method __str__."""
        assert str(self.model) == 'test_method: test_path'


class TestAbstractLogEntry:
    """Tests for AbstractHTTPStub class through LogEntry."""

    model = LogEntry()

    def test_str(self):
        """Test magic method __str__."""
        assert str(self.model) == ''
