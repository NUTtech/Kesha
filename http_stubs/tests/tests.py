from datetime import datetime
from http import HTTPStatus

import pytest

from http_stubs.models import HTTPMethod, LogEntry


class TestHTTPStubView:
    """Тестирование отображения http-заглушек."""

    @pytest.mark.parametrize('method', HTTPMethod.names())
    def test_nonexistent_stub(self, method: str, client):
        """Тест ответа, при ненайденной заглушке.

        В ответ должен приходить код 404.

        :param method: имя http метода
        :param client: фикстура http клиента
        """
        response = getattr(client, method.lower())('/nonexistent_stub')

        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize('method', HTTPMethod.names())
    def test_exist_not_regexp_stub(
        self, method: str, http_stub_factory, client,
    ):
        """Тест ответа, при имеющийся в безе не regex заглуше.

        :param method: имя http метода
        :param http_stub_factory: фабрика создания объектов HTTPStub
        :param client: фикстура http клиента
        """
        http_stub_factory(method=method)
        response = getattr(client, method.lower())('/default_path/')

        if method != HTTPMethod.HEAD.name:
            assert response.content == b'[]'
        assert response.status_code == HTTPStatus.OK
        assert response._headers['content-type'][1] == 'application/json'

    @pytest.mark.freeze_time('2020-05-25')
    def test_write_log(self, http_stub_factory, client):
        """Тестирует запись в лог запросов.

        :param http_stub_factory: фабрика создания объектов HTTPStub
        :param client: фикстура http клиента
        """
        content_type = 'text/plain'
        http_body = http_stub_factory(method=HTTPMethod.POST.name)
        client.post('/default_path/', 'test', content_type=content_type)
        log = LogEntry.objects.last()

        def _datefmt(date) -> str:  # noqa:WPS430
            """Преобразует объект даты в строку.

            Нужно для корректного сравнения datetime и FakeDateTime.

            :param date: объект даты для преобразования
            :returns: строка после применения шаблона
            """
            return date.strftime('%d%m%y')  # noqa:WPS323

        assert log.source_ip == '127.0.0.1'
        assert _datefmt(log.date) == _datefmt(datetime(2020, 5, 25))
        assert log.headers == {
            'Content-Length': '4',
            'Content-Type': content_type,
            'Cookie': '',
        }
        assert log.body == 'test'
        assert log.http_stub == http_body
        assert log.method == HTTPMethod.POST.name
        assert log.path == 'http://testserver/default_path/'

    @pytest.mark.parametrize('method', HTTPMethod.names())
    def test_exist_regexp_stub(self, method: str, http_stub_factory, client):
        """Тест ответа, при имеющийся в безе regex заглуше.

        :param method: имя http метода
        :param http_stub_factory: фабрика создания объектов HTTPStub
        :param client: фикстура http клиента
        """
        resp_body = 'Test Body'
        resp_status = 244
        resp_content_type = 'text/plain'
        resp_headers = {
            'X_TEST_HEADER_1': '1',
            'X_TEST_HEADER_2': 'test',
        }
        http_stub_factory(
            method=method,
            path=r'/test/\d+/',
            regex_path=True,
            resp_body=resp_body,
            resp_status=resp_status,
            resp_content_type=resp_content_type,
            resp_headers=resp_headers,
        )
        resp_method = method.lower()
        response = getattr(client, resp_method)('/test/100500/')

        if method != HTTPMethod.HEAD.name:
            assert response.content == resp_body.encode('utf-8')
        assert response.status_code == resp_status
        assert response._headers['content-type'][1] == resp_content_type
        for header_name, header_value in resp_headers.items():
            assert response._headers[header_name.lower()][1] == header_value

    @pytest.mark.parametrize(
        'regexp, path, status_code', (
            ('.*', '/test/', HTTPStatus.OK),
            ('.*', '/123/', HTTPStatus.OK),
            ('/test/', '/123/', HTTPStatus.NOT_FOUND),
            ('/test/', '/test/', HTTPStatus.OK),
            (r'/test/\d', '/test/1', HTTPStatus.OK),
            (r'/test/\d/', '/test/11/', HTTPStatus.NOT_FOUND),
            (r'/test/\d+/', '/test/11/', HTTPStatus.OK),
            (r'/\w{3}/\d{2}/(a|b)/[^a-z]+', '/tes/11/a/1', HTTPStatus.OK),
            (
                r'/\w{3}/\d{2}/(a|b)/[^a-z]+',
                '/tes/11/c/1',
                HTTPStatus.NOT_FOUND,
            ),
            (
                r'/\w{3}/\d{2}/(a|b)/[^a-z]+',
                '/tes/11/a/a',
                HTTPStatus.NOT_FOUND,
            ),
        ),
    )
    def test_regexp_matching(
        self, regexp, path, status_code, client, http_stub_factory,
    ):
        """Проверяет корректность матчинга регулярок.

        :param regexp: регулярное выражение
        :param path: путь запроса
        :param status_code: ожидаемый статус ответа
        :param client: фикструра http-клиента
        :param http_stub_factory: фабрика http-заглушек
        """
        http_stub_factory(path=regexp, regex_path=True)
        response = client.get(path)
        assert response.status_code == status_code
