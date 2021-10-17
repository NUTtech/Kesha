from http_stubs.models import AbstractHTTPStub, AbstractLogEntry


class TestAbstractHTTPStub:
    """Tests for AbstractHTTPStub class"""

    model = AbstractHTTPStub(
        method='test_method',
        path='test_path'
    )

    def test__str__(self):
        """Test magic method __str__."""
        assert str(self.model) == 'test_method: test_path'


class TestAbstractLogEntry:
    """Tests for AbstractHTTPStub class"""

    model = AbstractLogEntry()

    def test__str__(self):
        """Test magic method __str__."""
        assert str(self.model) == ''

