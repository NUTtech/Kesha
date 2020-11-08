from typing import Dict

from django import template

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
