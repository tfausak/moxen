from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


@login_required
def delete_user(request):
    """Delete a user's account.
    """
    request.user.is_active = False
    request.user.save()
    logout(request)
    messages.success(request, 'Account deleted.')
    return redirect(reverse('index'))
