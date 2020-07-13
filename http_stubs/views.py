from time import sleep
from typing import Optional

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from http_stubs.models import HTTPStub, LogEntry


class HTTPStubView(View):
    """Отображение для обработки http заглушек.

    Заглушки ищутся в базе данных, преставляют собой модели HTTPStub.
    Если заглушка найдена, записывается событие в лог (LogEntry) и
    в ответ подставляются параметры из заглушки.
    Если заглушка не найдена, возвращается 404.
    """

    def find_stub(self, method: str, path: str) -> Optional[HTTPStub]:
        """Ищет подходящую http-заглушку.

        :param method: имя метода запроса
        :param path: путь запроса
        :returns: Подходящая заглушка или None
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
        """Обработать входящий реквест.

        :param request: входящий http запрос
        :param args: парметры запроса
        :param kwargs: именнованные аргументы запроса
        :returns: ответ на http запрос
        """
        stub = self.find_stub(request.method, f'/{kwargs["path"]}')
        if not stub:
            return HttpResponseNotFound()
        LogEntry.objects.create(
            path=request.build_absolute_uri(),
            method=request.method,
            source_ip=request.META['REMOTE_ADDR'],
            body=request.body.decode('utf-8'),
            headers=dict(request.headers),
            http_stub=stub,
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
