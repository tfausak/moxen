from django.contrib.sites.models import Site


def site(_):
    """Add the current site to the context.
    """
    return {'site': Site.objects.get_current()}
