"""
Decorators for admin/manager access control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Only allow admin/staff users to access the view"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Tizimga kirishingiz kerak.")
            return redirect('accounts:login')
        if not (request.user.is_staff or request.user.user_type == 'admin'):
            messages.error(request, "Sizda ruxsat yo'q.")
            return redirect('catalog:home')
        return view_func(request, *args, **kwargs)
    return wrapper
