from enum import Enum
from typing import Iterator, KeysView, Tuple

from django.contrib.postgres.fields import HStoreField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Lookup


class HTTPMethod(Enum):
    """Enumeration of the available HTTP methods."""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'

    @classmethod
    def names(cls) -> KeysView[str]:
        """Set of the available HTTP method names.

        :returns: all names in the enumeration.
        """
        return cls.__members__.keys()

    @classmethod
    def slugs(cls) -> Iterator[Tuple[str, str]]:
        """Names of the methods for the model choice fields.

        :returns: iterator of tuples with http method names
        """
        return zip(cls.names(), cls.names())


class HTTPStub(models.Model):
    """HTTP stub."""

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
        choices=HTTPMethod.slugs(),
    )
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
    request_script = models.TextField(
        verbose_name='Request script',
        help_text='Language: python 3.8. The script will run on each request.',
        blank=True,
    )

    class Meta:
        verbose_name = 'http stub'
        verbose_name_plural = 'stubs'
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


class LogEntry(models.Model):
    """Log entry."""

    path = models.URLField(
        verbose_name='Full request path',
        max_length=2000,
    )
    method = models.CharField(
        verbose_name='Request method',
        max_length=10,
        choices=HTTPMethod.slugs(),
    )
    source_ip = models.GenericIPAddressField(
        verbose_name='Source IP',
    )
    date = models.DateTimeField(
        verbose_name='Request timestamp',
        auto_now_add=True,
        editable=False,
    )
    body = models.TextField(
        verbose_name='Request body',
    )
    headers = HStoreField(
        verbose_name='Request headers',
    )
    http_stub = models.ForeignKey(
        HTTPStub,
        verbose_name='Related stub',
        related_name='logs',
        blank=True,
        on_delete=models.CASCADE,
    )
    result_script = models.CharField(
        verbose_name='Result script',
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'

    def __str__(self) -> str:
        """Return string representation of the model.

        :returns: empty string to make admin look cleaner
        """
        return ''


@models.CharField.register_lookup
class RegExpLookup(Lookup):
    """Regular expression field lookup.

    Here's an example of how to use it:
    ```
    HTTPStub.objects.filter(path__match='/path/to/target/')
    ```
    """

    lookup_name = 'match'

    def as_postgresql(self, compiler, connection) -> Tuple[str, list]:
        """Compiles request for postgres.

        :param compiler: sql expression compiler
        :param connection: database connection
        :return: generated expression with params
        """
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return f'{rhs} ~ {lhs}', lhs_params + rhs_params
