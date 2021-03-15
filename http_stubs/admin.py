import json

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from http_stubs import models

admin.site.site_title = 'Kesha'
admin.site.site_header = 'Kesha Admin'


class LogEntryAdminBase(admin.ModelAdmin):
    """Base admin for LogEntry and ProxyLogEntry."""

    def has_add_permission(self, *args, **kwargs) -> bool:
        """Forbids adding new entries.

        :param args: optional args
        :param kwargs: optional kwargs
        :returns: False
        """
        return False

    def pretty_str(self, s: str) -> str:
        """Jsonify a string if possible.

        :param s: a string
        :returns: jsonify string
        """
        try:
            body = json.loads(s)
        except json.JSONDecodeError:
            body = None
        else:
            body = json.dumps(body, indent=2)
        return body

    def pretty_request_body(self, instance) -> str:
        """Jsonify the request body if possible.

        :param instance: instance of a log entry
        :returns: jsonify body
        """
        return self.pretty_str(instance.request_body)

    pretty_request_body.short_description = 'Jsonify request body'

    def pretty_response_body(self, instance) -> str:
        """Jsonify the response body if possible.

        :param instance: instance of a log entry
        :returns: jsonify body
        """
        return self.pretty_str(instance.response_body)

    pretty_request_body.short_description = 'Jsonify request body'

    list_filter = ('request_date', 'method')
    search_fields = ('path', 'source_ip')
    list_display = ('pk', 'request_date', 'http_stub', 'source_ip')
    readonly_fields = (
        'pk',
        'request_date',
        'http_stub',
        'path',
        'method',
        'source_ip',
        'request_headers',
        'request_body',
        'pretty_request_body',
        'result_script',
    )


@admin.register(models.LogEntry)
class LogEntryAdmin(LogEntryAdminBase):
    """Log entries admin."""


@admin.register(models.ProxyLogEntity)
class ProxyLogEntryAdmin(LogEntryAdminBase):
    """Proxy log entries admin."""

    readonly_fields = LogEntryAdminBase.readonly_fields + (
        'response_date',
        'response_latency',
        'response_headers',
        'response_body',
        'pretty_response_body',
    )


class HTTPStubAdminBase(admin.ModelAdmin):
    """Base admin for HTTPStub and ProxyHTTPStub."""

    change_form_template = 'admin/http_stubs/httpstub/change_form.html'
    extra_buttons_style = 'background-color:#00b0ff;color:white'

    actions = ['enable_action', 'disable_action']

    def enable_action(self, request: HttpRequest, queryset: QuerySet):
        """Enable selected stubs.

        :param request: http request
        :param queryset: queryset of the selected objects
        """
        queryset.update(is_active=True)

    enable_action.short_description = ' Enable'
    enable_action.icon = 'fas fa-toggle-on'
    enable_action.style = extra_buttons_style

    def disable_action(self, request: HttpRequest, queryset: QuerySet):
        """Disable selected stubs.

        :param request: http request
        :param queryset: queryset of the selected objects
        """
        queryset.update(is_active=False)

    disable_action.short_description = ' Disable'
    disable_action.icon = 'fas fa-toggle-off'
    disable_action.style = extra_buttons_style

    list_display = ('pk', 'is_active', 'method', 'path')

    list_filter = ('is_active', 'path', 'method')


@admin.register(models.HTTPStub)
class HTTPStubAdmin(HTTPStubAdminBase):
    """HTTP stub admin."""

    list_filter = HTTPStubAdminBase.list_filter + ('resp_status',)


@admin.register(models.ProxyHTTPStub)
class ProxyHTTPStubAdmin(HTTPStubAdminBase):
    """Proxy HTTP stub admin."""
