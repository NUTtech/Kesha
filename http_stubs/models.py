from django.contrib.postgres.fields import HStoreField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class HTTPMethod(models.TextChoices):
    """Enumeration of the available HTTP methods."""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'


class AbstractHTTPStub(models.Model):
    """Abstract HTTP stub."""

    is_active = models.BooleanField(
        verbose_name='Enabled',
        default=True,
    )
    path = models.CharField(
        verbose_name='Request path',
        max_length=2000,
        db_index=True,
    )
    regex_path = models.BooleanField(
        verbose_name='REGEX path',
        help_text='Path is a regular expression',
        default=False,
    )
    method = models.CharField(
        verbose_name='Request method',
        max_length=10,
        db_index=True,
        choices=HTTPMethod.choices,
    )
    request_script = models.TextField(
        verbose_name='Request script',
        help_text='Language: python 3.8. The script will run on each request.',
        blank=True,
    )
    enable_logging = models.BooleanField(
        verbose_name='Logging',
        help_text='Enables logging of requests',
        default=False,
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=('path', 'method'), name='uniq-path-method',
            ),
        ]

    def __str__(self):
        """Return string representation of the model.

        :returns: e.g. `get: /test/`.
        """
        return f'{self.method}: {self.path}'


class HTTPStub(AbstractHTTPStub):
    """HTTP stub."""

    resp_delay = models.PositiveIntegerField(
        verbose_name='Response delay',
        help_text='In milliseconds',
        default=0,
    )
    resp_body = models.TextField(
        verbose_name='Response body',
        default='[]',
        blank=True,
    )
    resp_status = models.IntegerField(
        verbose_name='Response status',
        default=200,
        validators=(MinValueValidator(0), MaxValueValidator(600)),
    )
    resp_content_type = models.CharField(
        verbose_name='Response Content-Type',
        default='application/json',
        max_length=255,
    )
    resp_headers = HStoreField(
        verbose_name='Response headers',
        help_text='In JSON format',
        default=dict,
        blank=True,
    )

    class Meta:
        verbose_name = 'request http stub'
        verbose_name_plural = 'request stubs'


class ProxyHTTPStub(AbstractHTTPStub):
    """Proxy HTTP stub."""

    target_url = models.URLField(
        verbose_name='Target url',
    )
    allow_forward_query = models.BooleanField(
        verbose_name='Forward query params',
        default=False,
    )
    target_ssl_verify = models.BooleanField(
        verbose_name='Target SSL verify',
        default=True,
    )
    target_timeout = models.IntegerField(
        verbose_name='Target response timeout',
        help_text='In seconds',
        default=15,
    )
    target_method = models.CharField(
        verbose_name='Target request method',
        max_length=10,
        choices=HTTPMethod.choices,
    )
    target_headers = HStoreField(
        verbose_name='Target headers',
        help_text='In JSON format',
        default=dict,
        blank=True,
    )
    target_body = models.TextField(
        verbose_name='Target body',
        default='',
        blank=True,
    )

    class Meta:
        verbose_name = 'proxy http stub'
        verbose_name_plural = 'proxy stubs'


class AbstractLogEntry(models.Model):
    """Abstract log entry."""

    path = models.URLField(
        verbose_name='Full request path',
        max_length=2000,
    )
    method = models.CharField(
        verbose_name='Request method',
        max_length=10,
        choices=HTTPMethod.choices,
    )
    source_ip = models.GenericIPAddressField(
        verbose_name='Source IP',
    )
    request_date = models.DateTimeField(
        verbose_name='Request timestamp',
        auto_now_add=True,
        editable=False,
    )
    request_headers = HStoreField(
        verbose_name='Request headers',
    )
    request_body = models.TextField(
        verbose_name='Request body',
    )
    result_script = models.CharField(
        verbose_name='Result script',
        max_length=200,
        blank=True,
    )

    class Meta:
        abstract = True
        verbose_name = 'MUST BE DEFINED'
        verbose_name_plural = 'MUST BE DEFINED'

    def __str__(self) -> str:
        """Return string representation of the model.

        :returns: empty string to make admin look cleaner
        """
        return ''


class LogEntry(AbstractLogEntry):
    """Log entry."""

    http_stub = models.ForeignKey(
        HTTPStub,
        verbose_name='Related stub',
        related_name='logs',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'request log'
        verbose_name_plural = 'request logs'


class ProxyLogEntity(AbstractLogEntry):
    """Proxy log entry."""

    http_stub = models.ForeignKey(
        ProxyHTTPStub,
        verbose_name='Related proxy stub',
        related_name='logs',
        on_delete=models.CASCADE,
    )
    target_path = models.URLField(
        verbose_name='Full target path',
        max_length=2000,
    )
    response_latency = models.IntegerField(
        verbose_name='Response latency',
        help_text='In microseconds',
    )
    response_body = models.TextField(
        verbose_name='Response body',
        help_text='From target',
    )
    response_headers = HStoreField(
        verbose_name='Response headers',
        help_text='From target',
    )

    class Meta:
        verbose_name = 'proxy log'
        verbose_name_plural = 'proxy logs'
