from django import template
from django.template.defaultfilters import stringfilter
from urllib import urlencode
import re


register = template.Library()


@register.inclusion_tag('paginator.html', takes_context=True)
def paginator(context, adjacent_pages=5):
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


@register.filter
@stringfilter
def title(string):
    """Convert a string to title case.
    """
    # Convert to naive title case.
    string = string.title()

    # Convert some words back to lower case.
    words = ['a', 'adiyah', 'an', 'at', 'and', 'into', 'for', 'kanar', 'm',
        'o', 'of', 're', u'r\xfbf', 's', 'the', 'to', 'vs']
    pattern = ur'\b({0})\b'.format(u'|'.join(word for word in words))
    replacement = lambda match: match.group(1).lower()
    string = re.sub(pattern, replacement, string, flags=re.IGNORECASE)

    # Convert some words to all upper case.
    pattern = r'(^.|\b(?:[iv]+|dci)\b)'
    replacement = lambda match: match.group(1).upper()
    string = re.sub(pattern, replacement, string, flags=re.IGNORECASE)

    return string
