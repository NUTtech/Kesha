import json
from html import unescape
from json import JSONDecodeError
from typing import AnyStr, Dict, List, Optional
from urllib.parse import urlunparse

from django import template
from django.contrib.admin.helpers import Fieldset
from django.template.defaultfilters import stringfilter

Url = str

register = template.Library()


@register.simple_tag(takes_context=True, name='absolute')
def absolute_url(context: Dict, url: Url, fieldset: Fieldset) -> Optional[Url]:
    """Tag that returns an absolute url.

    :param context: context of request
    :param url: relative url
    :param fieldset: Fieldset that is used to get value of the 'regex_path'
                     field from the form
    :returns: absolute url
    """
    if not url or not fieldset:
        return ''
    request = context['request']
    form = fieldset.form
    if form.initial.get('regex_path'):
        return urlunparse(
            [request.scheme, request.get_host(), '', '', '', ''],
        )
    if not url.startswith('/'):
        url = f'/{url}'
    return request.build_absolute_uri(url)


@register.filter()
@stringfilter
def headers_to_list(headers: AnyStr) -> List:
    """Filter that creates a list from a string of headers(dict).

    Return a list of the lines in the string representation of the request
    headers.
    :param headers: string representation of the request headers
    :returns: list of individual headers string representation
    """
    try:
        headers = json.loads(unescape(headers).replace("'", '"'))
    except (TypeError, JSONDecodeError):
        return []
    return [
        f'{header}: {header_value}'
        for header, header_value in headers.items()
    ]
