from functools import wraps
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render as django_render


def render(request, template_name, context):
    ctx = default_context(request)
    ctx.update(context)
    return django_render(request, template_name, context=ctx)


def default_context(request: WSGIRequest):
    return {'user': request.user}


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
