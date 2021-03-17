import json
from typing import Optional

import requests
from billiard.exceptions import SoftTimeLimitExceeded
from RestrictedPython import (
    compile_restricted,
    limited_builtins,
    safe_builtins,
    utility_builtins,
)
from RestrictedPython.Guards import full_write_guard

from http_stubs.models import LogEntry
from parrot import celery_app

restricted_builtins = {'__builtins__': {
    'requests': requests,
    'json': json,
    '_getitem_': lambda dict_obj, key: dict_obj[key],
    '_write_': full_write_guard,
    **safe_builtins,
    **limited_builtins,
    **utility_builtins,
}}


@celery_app.task()
def run_request_script(
    script: str,
    request_body: str,
    log_id: Optional[int] = None,
) -> None:
    """Task for run custom scripts from http stubs.

    :param log_id: LogEntry.id
    :param script: HTTPStub.request_script
    :param request_body: text body from a request
    """
    log: Optional[LogEntry] = None
    if log_id is not None:
        log = LogEntry.objects.get(pk=log_id)

    loc = {'request_body': request_body, **restricted_builtins}
    byte_code = compile_restricted(script)
    try:
        exec(byte_code, loc, None)  # noqa: S102, WPS421
    except SoftTimeLimitExceeded:
        log_msg = 'Error: Execution time limit exceeded'
    except Exception as err:
        log_msg = f'Error: {err}'
    else:
        log_msg = 'Done'

    if log is not None:
        log.result_script = log_msg
        log.save()
