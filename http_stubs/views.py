from time import sleep
from typing import Optional

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from http_stubs.models import HTTPStub, LogEntry
from http_stubs.tasks import run_request_script


class HTTPStubView(View):
    """HTTP stub view.

    Searches for matching HTTPStub object in the database.
    Creates a LogEntry and sends a response from the stub if stub is found.
    Returns 404 if stub is not found.
    """

    def find_stub(self, method: str, path: str) -> Optional[HTTPStub]:
        """Search for matching http stub.

        :param method: request method name
        :param path: request path
        :returns: matching stub or None
        """
        method = method.upper()
        stub = HTTPStub.objects.filter(
            method=method, path=path,
        ).exclude(regex_path=True).first()

        if stub:
            return stub

        return HTTPStub.objects.filter(
            method=method, path__match=path,
        ).exclude(regex_path=False).first()

    @csrf_exempt
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Process incoming request.

        :param request: incoming http request
        :param args: request args
        :param kwargs: request kwargs
        :returns: http response
        """
        stub = self.find_stub(request.method, request.get_full_path())
        if not stub:
            return HttpResponseNotFound()

        log = None

        if stub.enable_logging:
            log = LogEntry.objects.create(
                path=request.build_absolute_uri(),
                method=request.method,
                source_ip=request.META['REMOTE_ADDR'],
                body=request.body.decode('utf-8'),
                headers=dict(request.headers),
                http_stub=stub,
                result_script='Was launched' if stub.request_script else '',
            )

        if stub.request_script:
            run_request_script.delay(
                script=stub.request_script,
                request_body=request.body.decode('utf-8'),
                log_id=log.pk if log else None,
            )

        sleep(stub.resp_delay / 1000)
        response = HttpResponse(
            content=stub.resp_body,
            content_type=stub.resp_content_type,
            status=stub.resp_status,
        )

        for header_name, header_value in stub.resp_headers.items():
            response[header_name] = header_value

        return response
