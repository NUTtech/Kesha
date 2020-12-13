import json
from html import unescape
from json import JSONDecodeError
from typing import AnyStr, Dict, List

from django import template
from django.template.defaultfilters import stringfilter

Url = str

register = template.Library()


@register.simple_tag(takes_context=True, name='absolute')
def get_absolute_url_tag(context: Dict, url: Url) -> Url:
    """Tag that returns an absolute url.

    :param context: context of request
    :param url: relative url
    :returns: absolute url
    """
    return context.get('request').build_absolute_uri(url)


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
