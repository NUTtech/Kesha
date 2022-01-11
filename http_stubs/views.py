from string import Template
from time import sleep
from typing import Optional, Tuple, Union
from wsgiref.util import is_hop_by_hop

import requests
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from http_stubs.models import HTTPStub, LogEntry, ProxyHTTPStub, ProxyLogEntity
from http_stubs.tasks import run_request_script


def _request_body_decode(request: HttpRequest) -> str:
    """Decode a request body.

    :param request: a http request for getting decoded body
    :returns: decoded body or empty string
    """
    try:
        return request.body.decode(request.encoding or 'utf-8')
    except ValueError:
        return ''


def _httpstub_executor(  # noqa: WPS210
    stub: HTTPStub,
    request: HttpRequest,
) -> Tuple[HttpResponse, Optional[LogEntry]]:
    """Execute logic for HTTPStub instance.

    :param stub: a httpstub instance
    :param request: received request
    :returns: a response instance for return to requester
    """
    sleep(stub.resp_delay / 1000)

    request_body = _request_body_decode(request)

    tpl_ctx = {'body': request_body}

    for arg_name, arg_val in dict(request.GET).items():
        tpl_ctx[arg_name] = arg_val[0]

    response = HttpResponse(
        content=Template(stub.resp_body).safe_substitute(tpl_ctx),
        content_type=stub.resp_content_type,
        status=stub.resp_status,
    )

    for header_name, header_value in stub.resp_headers.items():
        response[header_name] = Template(header_value).safe_substitute(tpl_ctx)

    result_script = 'Was launched' if stub.request_script else ''

    log = LogEntry.objects.create(
        path=request.build_absolute_uri(),
        method=request.method,
        source_ip=request.META['REMOTE_ADDR'],
        request_headers=dict(request.headers),
        request_body=request_body,
        http_stub=stub,
        result_script=result_script,
        resp_status=stub.resp_status,
    ) if stub.enable_logging else None

    return response, log


def _proxy_httpstub_executor(  # noqa: WPS210
    stub: ProxyHTTPStub,
    request: HttpRequest,
) -> Tuple[HttpResponse, Optional[ProxyLogEntity]]:
    """Execute logic for ProxyHTTPStub instance.

    :param stub: a proxy stub instance
    :param request: received request
    :returns: a response instance for return to requester
    """
    t_request_args = {
        'method': request.method,
        'url': stub.target_url,
        'data': request.body,
        'verify': stub.target_ssl_verify,
        'timeout': stub.target_timeout,
    }
    if stub.allow_forward_query and (request.GET or request.POST):
        t_request_args['params'] = request.GET or request.POST
    if stub.target_headers:
        t_request_args['headers'] = stub.target_headers
    if stub.target_body:
        t_request_args['data'] = stub.target_body

    t_request_args['method'] = stub.target_method

    t_response = requests.request(**t_request_args)

    response = HttpResponse(
        content=t_response.content,
        content_type=t_response.headers['Content-Type'],
        status=t_response.status_code,
    )

    for header_name, header_value in t_response.headers.items():
        # skip headers which are meaningful
        # only for a single transport-level connection
        if is_hop_by_hop(header_name):
            continue
        response[header_name] = header_value

    log = ProxyLogEntity.objects.create(
        http_stub=stub,
        path=request.build_absolute_uri(),
        method=request.method,
        source_ip=request.META['REMOTE_ADDR'],
        request_headers=dict(request.headers),
        request_body=_request_body_decode(request),
        result_script='Was launched' if stub.request_script else '',
        target_path=t_response.request.url,
        response_latency=t_response.elapsed.microseconds,
        response_body=t_response.text,
        response_headers=dict(t_response.headers),
        resp_status=t_response.status_code,
    )

    return response, log


class HTTPStubView(View):
    """HTTP stub view.

    Searches for matching HTTPStub object in the database.
    Creates a LogEntry and sends a response from the stub if stub is found.
    Returns 404 if stub is not found.
    """

    stub_exec_map = {
        HTTPStub: _httpstub_executor,
        ProxyHTTPStub: _proxy_httpstub_executor,
    }

    @csrf_exempt
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Process incoming request.

        :param request: incoming http request
        :param args: request args
        :param kwargs: request kwargs
        :returns: http response
        """
        stub = self._find_stub(request.method, request.get_full_path())
        if not stub:
            return HttpResponseNotFound()

        response, log = self.stub_exec_map[stub.__class__](stub, request)

        if stub.request_script:
            run_request_script.delay(
                script=stub.request_script,
                request_body=_request_body_decode(request),
                log_id=log.pk if log else None,
            )

        return response

    def _find_stub(
        self,
        method: str,
        path: str,
    ) -> Optional[Union[HTTPStub, ProxyHTTPStub]]:
        """Search for matching http stub.

        :param method: request method name
        :param path: request path
        :returns: matching stub or None
        """
        method = method.upper()
        stub_models = (HTTPStub, ProxyHTTPStub)

        for model in stub_models:
            stub = model.objects.exclude(regex_path=True).filter(
                method=method, path=path,
            ).first()
            if stub:
                return stub

        for s_model in stub_models:
            stub = s_model.objects.exclude(regex_path=False).filter(
                method=method, path__match=path,
            ).first()
            if stub:
                return stub

        return None
