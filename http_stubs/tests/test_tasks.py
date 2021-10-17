from unittest.mock import patch

import pytest
from billiard.exceptions import SoftTimeLimitExceeded

from http_stubs.tasks import run_request_script


@pytest.mark.parametrize(
    'script, expect', (
        # valid scripts
        ('a = 1', 'Done'),
        (
            'def func(*args, **kwargs):\n'
            "    return json.dumps({'fake': 'data'})\n"
            '\n'
            'parsed_json = json.loads(func())\n'
            "assert parsed_json['fake'] == 'data'\n",
            'Done',
        ),

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
    run_request_script.delay(script=script, request_body='', log_id=log.id)
    log.refresh_from_db()
    assert log.result_script == expect


@pytest.mark.parametrize('script', ('a = 1', '1 / 0'))
def test_run_without_log(script):
    """Tests run task without log_id.

    :param script: a request script
    """
    run_request_script.run(script=script, request_body='')


@patch('http_stubs.tasks.compile_restricted')
def test_run_request_script_time_limit(compile_restricted, log_entity_factory):
    """Test SoftTimeLimitExceeded Exception in run_request_script."""
    compile_restricted.side_effect = SoftTimeLimitExceeded
    log = log_entity_factory()
    run_request_script.delay(script='', request_body='', log_id=log.id)
    log.refresh_from_db()
    assert log.result_script == 'Error: Execution time limit exceeded'
