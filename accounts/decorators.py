from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """Only Admin-role users (or superusers) may pass."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_admin_role:
            messages.error(request, "You need an admin account to do that.")
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return _wrapped
