from functools import wraps
from typing import Callable as function
from apps.core.choices import Roles
from rest_framework import status
from apps.core.exceptions import error_response


def role_required(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return error_response("You must be logged in", status.HTTP_401_UNAUTHORIZED)
            if request.user.role != required_role:
                return error_response("Permission denied", status.HTTP_403_FORBIDDEN)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_permission(view_func: function):
    return role_required(Roles.ADMIN)(view_func)

def member_permission(view_func: function):
    return role_required(Roles.MEMBER)(view_func)
