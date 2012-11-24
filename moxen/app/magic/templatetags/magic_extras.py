# pylint: disable=C0103
from django import template
from django.template.defaultfilters import stringfilter
import re


register = template.Library()


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
