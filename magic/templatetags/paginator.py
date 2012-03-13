"""Custom Django template tags.
"""
from django import template
from urllib import urlencode


register = template.Library()


@register.inclusion_tag('paginator.html', takes_context=True)
def paginator(context, adjacent_pages=5):
    """Add useful pagination variables.
    """
    context['pages'] = [page_ for page_ in range(
        context['page_obj'].number - adjacent_pages,
        context['page_obj'].number + adjacent_pages + 1
    ) if page_ > 0 and page_ <= context['paginator'].num_pages]
    context['show_first_page'] = 1 not in context['pages']
    context['show_last_page'] = context['paginator'].num_pages not in \
        context['pages']

    return context


@register.simple_tag(takes_context=True)
def page(context, page_):
    """Create a page link.

    This is necessary to prevent page links from clobbering other GET
    variables.
    """
    get = context['request'].GET.copy()
    get['page'] = page_
    return '?' + urlencode(get)
