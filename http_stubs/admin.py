from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from http_stubs import models

admin.site.site_title = 'Parrot'
admin.site.site_header = 'Parrot Admin'


class LogEntryMixin:
    """Миксин для админки и инлайна логов.

    Запрещает добавлять новые логи и редактировать старые.
    """

    def get_readonly_fields(self, *args, **kwargs) -> list:
        """Делаем все поля только для чтения.

        Генерируем список из всех полей, чтобы добавленные в будущем
        тоже сюда попали.

        :param args: опциональные аргументы
        :param kwargs: опциональные именованные аргументы
        :returns: Сгенерированный список.
        """
        return [field.name for field in self.model._meta.fields]  # noqa:WPS437

    def has_add_permission(self, *args, **kwargs) -> bool:
        """
        Запрещаем добавление новых записей руками.

        :param args: опциональные аргументы
        :param kwargs: опциональные именованные аргументы
        :returns: False
        """
        return False


class LogEntryAdminInline(LogEntryMixin, admin.TabularInline):
    """Инлайн логов для админки http заглушек."""

    model = models.LogEntry
    ordering = ('-date',)


@admin.register(models.LogEntry)
class LogEntryAdmin(LogEntryMixin, admin.ModelAdmin):
    """Админка логов."""

    list_display = ('pk', 'date', 'http_stub', 'source_ip')

    list_filter = ('date', 'method', 'path', 'source_ip')


@admin.register(models.HTTPStub)
class HTTPStubAdmin(admin.ModelAdmin):
    """Админка http заглушки."""

    extra_buttons_style = 'background-color:#00b0ff;color:white'

    actions = ['enable_action', 'disable_action']

    def enable_action(self, request: HttpRequest, queryset: QuerySet):
        """Экшн включающий выбранные заглушки.

        :param request: http запрос
        :param queryset: кверисет выбранных объектов
        """
        queryset.update(is_active=True)

    enable_action.short_description = ' Включить'
    enable_action.icon = 'fas fa-toggle-on'
    enable_action.style = extra_buttons_style

    def disable_action(self, request: HttpRequest, queryset: QuerySet):
        """Экшн выключающий выбранные заглушки.

        :param request: http запрос
        :param queryset: кверисет выбранных объектов
        """
        queryset.update(is_active=False)

    disable_action.short_description = ' Выключить'
    disable_action.icon = 'fas fa-toggle-off'
    disable_action.style = extra_buttons_style

    list_display = ('pk', 'is_active', 'method', 'path')

    list_filter = ('is_active', 'path', 'method', 'resp_status')

    inlines = (LogEntryAdminInline,)
