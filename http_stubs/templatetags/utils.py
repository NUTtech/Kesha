from django import template

register = template.Library()


@register.simple_tag(takes_context=True, name='absolute')
def get_absolute_url_tag(context, url):
    """Tag that returns an absolute url."""
    return context.get('request').build_absolute_uri(url)
