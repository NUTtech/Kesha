import pytest

from http_stubs.tasks import run_request_script


@pytest.mark.parametrize(
    'script, expect', (
        # valid scripts
        ('a = 1', 'Done'),
        ("""
def func(*args, **kwargs):
    return json.dumps({'fake': 'data'})

parsed_json = json.loads(func())
assert parsed_json['fake'] == 'data'
        """, 'Done'),  # noqa: WPS319

        # scripts with syntax error
        ('a = no_def', "Error: name 'no_def' is not defined"),

        # scripts with a exception
        ('1 / 0', 'Error: division by zero'),

        # unsafe scripts
        ('import os', 'Error: __import__ not found'),
    ),
)
def test_run_request_script(script, expect, log_entity_factory):
    """Checking a script launch.

    :param script: a request script
    :param expect: a expect result
    :param log_entity_factory: a factory for make LogEntity
    """
    log = log_entity_factory()
    run_request_script.delay(log_id=log.id, script=script, request_body='')
    log.refresh_from_db()
    assert log.result_script == expect
