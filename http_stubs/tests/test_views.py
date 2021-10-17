from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.http import HttpRequest, HttpResponse
from requests import Response, Request

from http_stubs.models import HTTPMethod, LogEntry
from http_stubs.views import _proxy_httpstub_executor


class TestHTTPStubView:
    """Tests representation of the http stubs."""

    @pytest.mark.parametrize('method', HTTPMethod.values)
    def test_nonexistent_stub(self, method: str, client):
        """Tests response when stub is not found.

        404 error should be returned.

        :param method: http method name
        :param client: http client fixture
        """
        response = getattr(client, method.lower())('/nonexistent_stub')

        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize('method', HTTPMethod.values)
    def test_exist_not_regexp_stub(
        self, method: str, http_stub_factory, client,
    ):
        """Tests response for non-regex stub.

        :param method: http method name
        :param http_stub_factory: HTTPStub factory
        :param client: http client fixture
        """
        http_stub_factory(method=method)
        response = getattr(client, method.lower())('/default_path/')

        if method != HTTPMethod.HEAD.name:
            assert response.content == b'[]'
        assert response.status_code == HTTPStatus.OK
        assert response._headers['content-type'][1] == 'application/json'

    @pytest.mark.freeze_time('2020-05-25')
    def test_write_log(self, http_stub_factory, client):
        """Tests request logging.

        :param http_stub_factory: HTTPStub factory
        :param client: http client fixture
        """
        content_type = 'text/plain'
        http_stub = http_stub_factory(
            method=HTTPMethod.POST.name,
            path='/regex/',
            regex_path=True,
            request_script='a = 1',
            enable_logging=True,
        )

        request_path = f'/regex/?query={"search" * 300}'

        client.post(request_path, 'test', content_type=content_type)
        log = LogEntry.objects.last()

        def _datefmt(date) -> str:  # noqa:WPS430
            """Convert date object to string.

            For comparing datetime and FakeDateTime.

            :param date: date object
            :returns: string representation of the input date
            """
            return date.strftime('%d%m%y')  # noqa:WPS323

        assert log.source_ip == '127.0.0.1'
        assert _datefmt(log.request_date) == _datefmt(datetime(2020, 5, 25))
        assert log.request_headers == {
            'Content-Length': '4',
            'Content-Type': content_type,
            'Cookie': '',
        }
        assert log.request_body == 'test'
        assert log.http_stub == http_stub
        assert log.method == HTTPMethod.POST.name
        assert log.path == f'http://testserver{request_path}'
        assert log.result_script == 'Done'

    def test_empty_log(self, http_stub_factory, client):
        """Tests http stub without logs.

        :param http_stub_factory: HTTPStub factory
        :param client: http client fixture
        """
        stub_path = '/test/'
        http_stub_factory(method=HTTPMethod.POST.name, path=stub_path)
        response = client.post(stub_path)
        assert response.status_code == HTTPStatus.OK
        assert LogEntry.objects.last() is None

    @pytest.mark.parametrize('method', HTTPMethod.values)
    def test_exist_regexp_stub(self, method: str, http_stub_factory, client):
        """Tests response for the regex stub.

        :param method: http method name
        :param http_stub_factory: HTTPStub factory
        :param client: http client fixture
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
            path=r'/test/\d+/\?arg=\w+',
            regex_path=True,
            resp_body=resp_body,
            resp_status=resp_status,
            resp_content_type=resp_content_type,
            resp_headers=resp_headers,
        )
        resp_method = method.lower()
        response = getattr(client, resp_method)('/test/100500/?arg=test')

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
        """Tests correctness of the regex matching.

        :param regexp: regular expression
        :param path: request path
        :param status_code: expected response status code
        :param client: http client fixture
        :param http_stub_factory: HTTPStub factory
        """
        http_stub_factory(path=regexp, regex_path=True)
        response = client.get(path)
        assert response.status_code == status_code

    @patch('http_stubs.views.requests.request')
    def test_proxy_httpstub_executor(
        self,
        mock_request_func,
        proxy_http_stub_factory,
    ):
        request = HttpRequest()
        request.method = HTTPMethod.OPTIONS.name
        request.path = '127.0.0.1/test_request_path'
        request.META['HTTP_TEST_HEADER'] = 'Value'
        request.META['SERVER_NAME'] = '127.0.0.1'
        request.META['SERVER_PORT'] = '80'
        request.META['REMOTE_ADDR'] = '192.168.1.42'
        request._body = b'test_body'
        request.GET['q'] = 'testParam'

        fake_response = Response()
        fake_response.headers['TEST_RESPONSE_HEADER'] = '1'
        fake_response.headers['Content-Type'] = 'text/plain'
        fake_response._content = b'I am a teapot'
        fake_response.status_code = 418
        fake_response.request = Request(url='target_url')
        mock_request_func.return_value = fake_response

        # test without additional params
        stub = proxy_http_stub_factory(target_url='test_target_url')
        _, _ = _proxy_httpstub_executor(stub, request)

        call_args = mock_request_func.call_args.kwargs
        assert call_args['method'] == HTTPMethod.GET.name
        assert call_args['url'] == stub.target_url
        assert call_args['headers']['Test-Header'] == 'Value'
        assert call_args['data'] == request._body
        assert call_args['verify'] is True
        assert call_args['timeout'] == 15

        stub = proxy_http_stub_factory(
            target_url='test_target_url',
            allow_forward_query=True,
            target_body='test target body',
            target_method=HTTPMethod.TRACE.name,
            target_headers={'test_target_header': 1},
        )

        response, log = _proxy_httpstub_executor(stub, request)

        log.refresh_from_db()

        call_args = mock_request_func.call_args.kwargs
        assert call_args['method'] == stub.target_method
        assert call_args['url'] == stub.target_url
        assert call_args['headers']['test_target_header'] == 1
        assert call_args['data'] == stub.target_body
        assert call_args['params']['q'] == 'testParam'

        assert response.status_code == fake_response.status_code
        assert response.content == fake_response.content
        assert response._headers['test_response_header'][1] == '1'

        assert log.http_stub_id == stub.pk
        assert log.path == 'http://127.0.0.1/test_request_path'
        assert log.method == request.method
        assert log.source_ip == request.META['REMOTE_ADDR']
        assert log.request_headers == {'Test-Header': 'Value'}
        assert log.request_body == 'test_body'
        assert log.result_script == ''
        assert log.target_path == fake_response.request.url
        assert log.response_latency == 0
        assert log.response_body == 'I am a teapot'
        assert log.response_headers == {
            'Content-Type': 'text/plain',
            'TEST_RESPONSE_HEADER': '1',
        }
