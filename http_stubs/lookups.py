from typing import Tuple

from django.db import models

__all__ = ['RegExpLookup']


@models.CharField.register_lookup
class RegExpLookup(models.Lookup):
    """Regular expression field lookup.

    Here's an example of how to use it:
    ```
    HTTPStub.objects.filter(path__match='/path/to/target/')
    ```
    """

    lookup_name = 'match'

    # lookup only works with PostgreSQL
    def as_sql(self, compiler, connection) -> Tuple[str, list]:  # noqa: D102
        raise NotImplementedError

    def as_postgresql(self, compiler, connection) -> Tuple[str, list]:
        """Compiles request for postgres.

        :param compiler: sql expression compiler
        :param connection: database connection
        :return: generated expression with params
        """
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        return f'{rhs} ~ {lhs}', lhs_params + rhs_params
