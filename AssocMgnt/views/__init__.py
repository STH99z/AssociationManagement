from functools import wraps
from django.http import HttpResponseRedirect


def require_role(role):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_anonymous:
                return HttpResponseRedirect('/')
            if not user.is_active:
                return HttpResponseRedirect('/')
            if user.role != role:
                return HttpResponseRedirect('/')
            return func(request, *args, **kwargs)

        return wrapper

    return wrapper_outer
