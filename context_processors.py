from django.contrib.sites.models import Site


def site(request):
    """Add the current site to the context.
    """
    return {'site': Site.objects.get_current()}
