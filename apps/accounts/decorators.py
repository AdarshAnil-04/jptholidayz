from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(*allowed_roles):
    def check_role(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.role == 'SUPER_ADMIN':
            return True
        return user.role in allowed_roles
    return user_passes_test(check_role)

def customer_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapped

def booking_staff_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_booking_staff or request.user.is_admin_owner):
            raise PermissionDenied("You do not have permission to access booking staff operations.")
        return view_func(request, *args, **kwargs)
    return wrapped

def content_manager_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_content_manager or request.user.is_admin_owner):
            raise PermissionDenied("You do not have permission to access content management operations.")
        return view_func(request, *args, **kwargs)
    return wrapped

def admin_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_owner:
            raise PermissionDenied("Only Administrators have access to this section.")
        return view_func(request, *args, **kwargs)
    return wrapped
