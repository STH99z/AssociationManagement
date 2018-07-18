from functools import wraps
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render as django_render
from AssocMgnt.models import StaffPermission


@wraps(django_render)
def render(request, template_name, context):
    ctx = default_context(request)
    ctx.update(context)
    return django_render(request, template_name, context=ctx)


def default_context(request: WSGIRequest):
    return {'user': request.user,
            'params': request.content_params}


def require_role(role: int):
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


def require_role_in_class(role: int):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper(class_inst, request, *args, **kwargs):
            user = request.user
            if user.is_anonymous:
                return HttpResponseRedirect('/')
            if not user.is_active:
                return HttpResponseRedirect('/')
            if user.role != role:
                return HttpResponseRedirect('/')
            return func(class_inst, request, *args, **kwargs)

        return wrapper

    return wrapper_outer


def check_permission(request, register: bool = False, event: bool = False, location: bool = False,
                     bulletin: bool = False):
    user = request.user
    perm = StaffPermission.objects.get(staff_id=user.id)
    if perm is None:
        return False
    if register:
        if not perm.registration_perm:
            return False
    if event:
        if not perm.event_perm:
            return False
    if location:
        if not perm.location_perm:
            return False
    if bulletin:
        if not perm.bulletin_perm:
            return False
    return True


def require_permission(register: bool = False, event: bool = False, location: bool = False, bulletin: bool = False):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            from AssocMgnt.template_models import tInfo
            user = request.user
            perm = StaffPermission.objects.get(staff_id=user.id)
            if perm is None:
                return render(request, 'big_info.html',
                              {'info': tInfo('操作失败！', '你没有操作权限，请联系管理员为你提升操作权限。', href='/staff/app/list/',
                                             palette='warning')})
            if register:
                if not perm.registration_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            if event:
                if not perm.event_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            if location:
                if not perm.location_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            if bulletin:
                if not perm.bulletin_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            return func(request, *args, **kwargs)

        return wrapper

    return wrapper_outer


def require_permission_in_class(register: bool = False, event: bool = False, location: bool = False,
                                bulletin: bool = False):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper(class_inst, request, *args, **kwargs):
            from AssocMgnt.template_models import tInfo
            user = request.user
            perm = StaffPermission.objects.filter(staff_id=user.id).first()
            if perm is None:
                return render(request, 'big_info.html',
                              {'info': tInfo('操作失败！', '你没有操作权限，请联系管理员为你提升操作权限。', href='/staff/app/list/',
                                             palette='warning')})
            if register:
                if not perm.registration_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            if event:
                if not perm.event_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            if location:
                if not perm.location_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            if bulletin:
                if not perm.bulletin_perm:
                    return render(request, 'big_info.html',
                                  {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                                 palette='warning')})
            return func(class_inst, request, *args, **kwargs)

        return wrapper

    return wrapper_outer
