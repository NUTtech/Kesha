import pytest

from http_stubs import RegExpLookup


def test_regexplookup_assql():
    """Smoke test for as_sql method in RegExpLookup."""
    with pytest.raises(NotImplementedError):
        RegExpLookup.as_sql('', '', '')
