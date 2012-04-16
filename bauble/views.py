from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile(request):
    """Display a user's profile.
    """
    return render(request, 'magic/profile.html')
