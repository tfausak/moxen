# pylint: disable=C0103
from django import template
from urllib import urlencode


register = template.Library()


@register.inclusion_tag('moxen/paginator.html', takes_context=True)
def paginator(context, adjacent_pages=3):
    """Add useful pagination variables.
    """
    context['pages'] = [page for page in range(
        context['page_obj'].number - adjacent_pages,
        context['page_obj'].number + adjacent_pages + 1
    ) if page > 0 and page <= context['paginator'].num_pages]
    context['show_first_page'] = 1 not in context['pages']
    context['show_last_page'] = context['paginator'].num_pages not in \
        context['pages']

    return context


@register.simple_tag(takes_context=True)
def link(context, key, value):
    """Create a link by appending to the query string.

    If the key already exists in the query string, it will be updated.
    """
    get = context['request'].GET.copy()
    get[key] = value
    return '?' + urlencode(get)
