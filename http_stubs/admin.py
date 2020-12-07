import json

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from http_stubs import models

admin.site.site_title = 'Parrot'
admin.site.site_header = 'Parrot Admin'


@admin.register(models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Log entries admin."""

    def get_readonly_fields(self, *args, **kwargs) -> list:
        """Mark all fields read-only.

        Generates list of all fields so that fields added in future would be
        also added here.

        :param args: optional args
        :param kwargs: optional kwargs
        :returns: list of fields.
        """
        fields = [field.name for field in self.model._meta.fields
                  if field.name not in self.exclude]
        return fields + list(self.readonly_fields)

    def has_add_permission(self, *args, **kwargs) -> bool:
        """Forbids adding new entries.

        :param args: optional args
        :param kwargs: optional kwargs
        :returns: False
        """
        return False

    def pretty_body(self, instance):
        """Jsonify the request body if possible."""
        try:
            body = json.loads(instance.body)
        except json.JSONDecodeError:
            body = None
        else:
            body = json.dumps(body, indent=2)
        return body

    pretty_body.short_description = 'Jsonify request body'

    list_display = ('pk', 'date', 'http_stub', 'source_ip')
    list_filter = ('date', 'method')
    search_fields = ('path', 'source_ip')
    readonly_fields = ('body', 'pretty_body')


@admin.register(models.HTTPStub)
class HTTPStubAdmin(admin.ModelAdmin):
    """HTTP stub admin."""

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

    list_filter = ('is_active', 'path', 'method', 'resp_status')
