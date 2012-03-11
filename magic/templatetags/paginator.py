"""Custom Django template tags.
"""
from django import template


register = template.Library()


@register.inclusion_tag('paginator.html', takes_context=True)
def paginator(context, adjacent_pages=1):
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
