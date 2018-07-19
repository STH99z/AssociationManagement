from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from AssocMgnt.models import *
from AssocMgnt.template_models import *
from . import render, require_role, require_permission, require_role_in_class, require_permission_in_class, \
    check_permission
from django.template import Template, Engine, Context
from django.shortcuts import get_list_or_404, get_object_or_404
from pytz import timezone
from .founder_views import fromRequest
import logging

engine = Engine.get_default()
logger = logging.getLogger(__name__)


@require_role(User.ROLE_STAFF)
def assoc_list(req: WSGIRequest):
    assoc_list = Association.objects.filter(created=True) \
        .exclude(deletionMark=True, deletionTime__lt=utcnow()).all()
    return render(req, 'staff/assoc_list.html',
                  {'assoc_list': assoc_list})


@require_role(User.ROLE_STAFF)
def assoc_id(req: WSGIRequest, assoc_id: int):
    assoc = get_object_or_404(Association, id=assoc_id)
    if assoc.created == False:
        return render(req, 'big_info.html',
                      {'info': tInfo('访问失败！', '这个社团还没有被审批创建，不能访问。', href='/staff/app/list/', palette='warning')})
    assoc.displayAll = True
    return render(req, 'staff/assoc_id.html',
                  {'assoc': assoc,
                   'assoc_id': assoc_id,
                   'members': Member.objects.filter(association_id=assoc_id).all()})


@require_role(User.ROLE_STAFF)
def assoc_id_bulletin(req: WSGIRequest, assoc_id: int):
    messages = BulletinApplication.objects.filter(starterAssociation_id=assoc_id, result=1).all()
    return render(req, 'staff/assoc_id_bulletin.html',
                  {'messages': messages,
                   'assoc_id': assoc_id})


class assoc_id_dismiss_class(View):
    @require_role_in_class(User.ROLE_STAFF)
    def get(self, req: WSGIRequest, assoc_id: int):
        assoc = get_object_or_404(Association, id=assoc_id)
        assoc.displayAll = True
        deletionTime = utcnow() + timedelta(days=7)
        return render(req, 'staff/assoc_id_dismiss.html',
                      {'assoc': assoc,
                       'assoc_id': assoc_id,
                       'deletionTime': deletionTime.strftime('%Y-%m-%dT%H:%M'),
                       'button': tSubmitButton(text='设置解散警告')})

    @require_role_in_class(User.ROLE_STAFF)
    @require_permission_in_class(True, False, False, False)
    def post(self, req: WSGIRequest, assoc_id: int):
        kw = fromRequest(req)
        kw['deletionMark'] = True
        assoc = get_object_or_404(Association, id=assoc_id)
        assoc.update(**kw)
        assoc.save()
        return render(req, 'big_info.html',
                      {'info': tInfo('已发送警告', '点击按钮返回', href='')})


@require_role(User.ROLE_STAFF)
def app_list(req: WSGIRequest, app_type: int = 0):
    app_type = [RegistrationApplication, EventApplication, LocationApplication, BulletinApplication][app_type]
    app1_list = app_type.objects.filter(result=0).all()
    app2_list = app_type.objects.filter(result=2).all()
    app3_list = app_type.objects.filter(result=1).all()
    return render(req, 'staff/app_list.html',
                  {'app1_list': app1_list,
                   'app2_list': app2_list,
                   'app3_list': app3_list})


def utcnow():
    return datetime.utcnow().replace(tzinfo=timezone('UTC'))


class app_id_class(View):
    @require_role_in_class(User.ROLE_STAFF)
    def get(self, req: WSGIRequest, app_id: int):
        app_type = int(req.GET['type'])
        app_type = [RegistrationApplication, EventApplication, LocationApplication, BulletinApplication][app_type]
        app = get_object_or_404(app_type, id=app_id)
        b = utcnow()
        return render(req, 'staff/app_id.html',
                      {'app': app,
                       'details': True,
                       'button': tSubmitButton(text='提交审核', href=''),
                       'now': b})

    @require_role_in_class(User.ROLE_STAFF)
    def post(self, req: WSGIRequest, app_id: int):
        kw = fromRequest(req)
        kw['reviewTime'] = utcnow()
        app_type = int(req.GET['type'])
        app_type = [RegistrationApplication, EventApplication, LocationApplication, BulletinApplication][app_type]
        app = get_object_or_404(app_type, id=app_id)

        check = check_permission(req,
                                 isinstance(app, RegistrationApplication),
                                 isinstance(app, EventApplication),
                                 isinstance(app, LocationApplication),
                                 isinstance(app, BulletinApplication))
        if not check:
            return render(req, 'big_info.html',
                          {'info': tInfo('操作失败！', '你没有这项操作权限。如果需要，联系系统管理员以提升权限。', href='/staff/app/list/',
                                         palette='warning')})

        print(kw)

        if isinstance(app, RegistrationApplication):
            if kw['result'] == '1':
                app.association.created = True
                app.association.createTime = utcnow()
                app.association.save()
            elif kw['result'] == '0':
                if app.association.created:
                    return render(req, 'big_info.html',
                                  {'info': tInfo('操作失败！', '请使用解散功能消去已经通过审核的社团。', href='', palette='warning')})
        if isinstance(app, LocationApplication):
            if kw['result'] == '1':
                loc_apps = LocationApplication.objects.filter(location_id=app.location_id, result=1).all()
                for loc2 in loc_apps:
                    if intersect((app.fromTime, app.toTime), (loc2.fromTime, loc2.toTime)):
                        return render(req, 'big_info.html',
                                      {'info': tInfo('操作失败！', '时间段和%s的时间段冲突！' % loc2.title,
                                                     href='', palette='warning')})
        if isinstance(app, EventApplication):
            if app.toTime <= utcnow() and kw['confirmHeld'] == 'False':
                print('扣除10点')
                app.starterAssociation.credit -= 10
                app.starterAssociation.save()
        if kw.get('holdingTime', '') == '':
            kw['holdingTime'] = None
        app.update(**kw)
        app.save()
        return render(req, 'big_info.html',
                      {'info': tInfo('审核成功！', '您和该社团负责人都会看到更改。', href='')})


def intersect(tup1, tup2):
    a, b = tup1
    c, d = tup2
    l, r = max(a, c), min(b, d)
    return True if (l <= r) else False


@require_role(User.ROLE_STAFF)
def app_id_export(req: WSGIRequest, app_id: int):
    pass


assoc_id_dismiss = assoc_id_dismiss_class.as_view()
app_id = app_id_class.as_view()
