from enum import Enum
from typing import Iterator, KeysView, Tuple

from django.contrib.postgres.fields import HStoreField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Lookup


class HTTPMethod(Enum):
    """Перечесление доступных http-методов."""

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
        """Множество доступных имён http-методов.

        :returns: все имена вариантов перечисления
        """
        return cls.__members__.keys()

    @classmethod
    def slugs(cls) -> Iterator[Tuple[str, str]]:
        """Имена методов для choices полей моделей.

        :returns: итератор таплов имён http методов
        """
        return zip(cls.names(), cls.names())


class HTTPStub(models.Model):
    """HTTP заглушка."""

    is_active = models.BooleanField(
        verbose_name='Включено',
        default=True,
    )
    path = models.CharField(
        verbose_name='Путь запроса',
        max_length=2000,
        db_index=True,
    )
    regex_path = models.BooleanField(
        verbose_name='REGEX путь',
        help_text='Путь представлен регулярным выражением',
        default=False,
    )
    method = models.CharField(
        verbose_name='Метод запроса',
        max_length=10,
        db_index=True,
        choices=HTTPMethod.slugs(),
    )
    resp_delay = models.PositiveIntegerField(
        verbose_name='Задержка перед ответом',
        help_text='Задаётся в милисекундах',
        default=0,
    )
    resp_body = models.TextField(
        verbose_name='Тело ответа',
        default='[]',
        blank=True,
    )
    resp_status = models.IntegerField(
        verbose_name='Статус ответа',
        default=200,
        validators=(MinValueValidator(0), MaxValueValidator(600)),
    )
    resp_content_type = models.CharField(
        verbose_name='Content-type ответа',
        default='application/json',
        max_length=255,
    )
    resp_headers = HStoreField(
        verbose_name='Заголовки ответа',
        help_text='Заполняется в формате json',
        default=dict,
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
        """Строковое представление модели.

        :returns: пример `get: /test/`.
        """
        return f'{self.method}: {self.path}'


class LogEntry(models.Model):
    """Зпись лога."""

    path = models.URLField(
        verbose_name='Полный путь запроса',
    )
    method = models.CharField(
        verbose_name='Метод запроса',
        max_length=10,
        choices=HTTPMethod.slugs(),
    )
    source_ip = models.GenericIPAddressField(
        verbose_name='IP источника запроса',
    )
    date = models.DateTimeField(
        verbose_name='Время запроса',
        auto_now_add=True,
        editable=False,
    )
    body = models.TextField(
        verbose_name='Тело запроса',
    )
    headers = HStoreField(
        verbose_name='Заголовки запроса',
    )
    http_stub = models.ForeignKey(
        HTTPStub,
        verbose_name='Связанная заглушка',
        related_name='logs',
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'

    def __str__(self) -> str:
        """Cтроковое представление модели.

        :returns: возвращает пустую строку, чтобы убрать лишний вывод
                  в некоторых местах админки.
        """
        return ''


@models.CharField.register_lookup
class RegExpLookup(Lookup):
    """Лукап для поиска регулярных выражений в базе.

    Пример использования:
    ```
    HTTPStub.objects.filter(path__match='/path/to/target/')
    ```
    """

    lookup_name = 'match'

    def as_postgresql(self, compiler, connection) -> Tuple[str, list]:
        """Компиляция запроса для postgres.

        :param compiler: компилятор sql выражения
        :param connection: подключение к базе
        :return: сгенерированное выражение с параметрами
        """
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return f'{rhs} ~ {lhs}', lhs_params + rhs_params
