from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from AssocMgnt.models import *
from AssocMgnt.template_models import *
from . import render, require_role
from django.template import Template, Engine, Context
from django.shortcuts import get_list_or_404, get_object_or_404
import logging
from pytz import timezone

engine = Engine.get_default()
logger = logging.getLogger(__name__)


def fromRequest(request: WSGIRequest):
    kw = dict(request.POST)
    kw.pop('csrfmiddlewaretoken')
    for k, v in kw.items():
        kw[k] = v[0]
    return kw


def assoc_list(request: WSGIRequest):
    user = request.user
    assoc_list = Association.objects.filter(founder=user, created=True) \
        .exclude(deletionMark=True, deletionTime__lte=utcnow()).all()
    button = tAButton(text='申请创建社团', href='/founder/app/assoc/create')
    return render(request, 'founder/assoc_list.html',
                  {'assoc_list': assoc_list,
                   'button': button})


def assoc_id(request: WSGIRequest, assoc_id: int):
    assoc = get_object_or_404(Association, id=assoc_id)
    if assoc.created == False:
        return render(request, 'big_info.html',
                      {'info': tInfo('访问失败！', '这个社团还没有被审批创建，不能访问。', href='/founder/app/list/', palette='warning')})
    assoc.displayAll = True
    return render(request, 'founder/assoc_id.html',
                  {'assoc_id': assoc_id,
                   'assoc': assoc})


class assoc_id_edit(View):
    def get(self, request: WSGIRequest, assoc_id: int):
        assoc = get_object_or_404(Association, id=assoc_id)
        button = tSubmitButton(text='提交修改')
        return render(request, 'founder/assoc_id_edit.html',
                      {'button': button,
                       'assoc': assoc,
                       'assoc_id': assoc_id})

    def post(self, request: WSGIRequest, assoc_id: int):
        assoc = get_object_or_404(Association, id=assoc_id)
        kw = fromRequest(request)
        assoc.update(**kw)
        assoc.save()
        return render(request, 'big_info.html',
                      {'info': tInfo('修改已提交', '您可以返回立即看到修改。', href='')})


class assoc_id_members(View):
    def get(self, request: WSGIRequest, assoc_id: int):
        members = Member.objects.filter(association_id=assoc_id).all()
        button = tSubmitButton(text='添加成员')
        return render(request, 'founder/assoc_id_member.html',
                      {'button': button,
                       'members': members,
                       'assoc_id': assoc_id})

    def post(self, request: WSGIRequest, assoc_id: int):
        kw = fromRequest(request)
        m = Member(**kw)
        m.association_id = assoc_id
        m.save()
        return render(request, 'big_info.html',
                      {'info': tInfo('新成员已添加', '您可以返回立即看到修改。', href='')})


class assoc_id_bulletin(View):
    def get(self, request: WSGIRequest, assoc_id: int):
        button = tAButton(text='申请发布新公告', href='/founder/app/bulletin/create/')
        messages = BulletinApplication.objects.filter(starterAssociation_id=assoc_id, result=1).all()
        return render(request, 'founder/assoc_id_bulletin.html',
                      {'button': button,
                       'messages': messages,
                       'assoc_id': assoc_id})


def app_list(request: WSGIRequest, app_type: int = 0):
    href = ['/founder/app/assoc/create/',
            '/founder/app/event/create/',
            '/founder/app/location/create/',
            '/founder/app/bulletin/create/', ][app_type]
    app_type = [RegistrationApplication, EventApplication, LocationApplication, BulletinApplication][app_type]
    app1_list = app_type.objects.filter(starterUser=request.user, result=0).all()
    app2_list = app_type.objects.filter(starterUser=request.user, result=2).all()
    app3_list = app_type.objects.filter(starterUser=request.user, result=1).all()
    new_button = tAButton(text='创建新的申请', href=href)
    return render(request, 'founder/app_list.html',
                  {'app1_list': app1_list,
                   'app2_list': app2_list,
                   'app3_list': app3_list,
                   'new_button': new_button})


def app_id(request: WSGIRequest, app_id: int):
    return render(request, 'level1_founder.html', {})


class app_assoc_create(View):
    def get(self, request: WSGIRequest):
        user = request.user
        registerd_assoc_list = Association.objects.filter(created=True).all()
        return render(request, 'founder/assoc_create.html', {'registerd_assoc_list': registerd_assoc_list})

    def post(self, request: WSGIRequest):
        kw = fromRequest(request)
        kw['founder'] = request.user
        kw['parent'] = Association.objects.filter(id=request.POST.get('parent', '-1')).first()
        logger.info(kw)
        a = Association(**kw)
        a.save()
        b = RegistrationApplication.create_one(request.user, None, a)
        b.save()
        return render(request, 'big_info.html',
                      {'info': tInfo(title='申请已发送', text='请耐心给等待教务员工审核。', href='/founder/app/list/')})


def utcnow():
    return datetime.utcnow().replace(tzinfo=timezone('UTC'))


class app_event_create(View):
    def get(self, request: WSGIRequest):
        loc_app_list = LocationApplication.objects.filter(starterUser=request.user, result=1).all()
        return render(request, 'founder/event_create_.html',
                      {'loc_app_list': loc_app_list})

    def post(self, request: WSGIRequest):
        kw = fromRequest(request)
        print(kw)
        kw['starterUser'] = request.user
        kw['starterAssociation'] = Association.objects.filter(founder=request.user, created=True).first()
        kw['useLocation'] = kw.get('useLocation', 'off') == 'on'
        if kw.get('useLocation', False):
            if kw.get('locationApplication', -1) == -1:
                return render(request, 'big_info.html',
                              {'info': tInfo('申请失败！', '需要一个通过审核的场所使用申请！', href='', palette='warning')})
            kw['locationApplication'] = LocationApplication.objects.filter(id=kw['locationApplication']).first()
            print(kw['locationApplication'])
            # kw ['locationApplication_id'] = int(kw['locationApplication'])
        kw['title'] = '申请举办活动'
        kw['content'] = f'申请举办 “{kw["name"]}” 活动'

        print(kw)
        ea = EventApplication(**kw)
        ea.save()
        return render(request, 'big_info.html',
                      {'info': tInfo('申请已发送', '请耐心给等待教务员工审核。', href='/founder/app/list/1')})


class app_location_create(View):
    def get(self, request: WSGIRequest):
        loc_list = Location.objects.all()
        return render(request, 'founder/location_create.html',
                      {'loc_list': loc_list})

    def post(self, request: WSGIRequest):
        kw = fromRequest(request)
        print(kw)
        kw['starterUser'] = request.user
        kw['starterAssociation'] = Association.objects.filter(founder=request.user, created=True).first()
        if kw.get('location', -1) == -1:
            return render(request, 'big_info.html',
                          {'info': tInfo('申请失败！', '需要选择一个场所！', href='', palette='warning')})
        kw['location'] = get_object_or_404(Location, id=kw['location'])
        kw['title'] = '申请使用场所'
        kw['content'] = f'{kw["location"].name}'
        kw['shareLocation'] = kw.get('shareLocation', 'off') == 'on'
        la = LocationApplication(**kw)
        la.save()
        return render(request, 'big_info.html',
                      {'info': tInfo('申请已发送', '请耐心给等待教务员工审核。', href='/founder/app/list/2')})


class app_bulletin_create(View):
    def get(self, request: WSGIRequest):
        return render(request, 'founder/bulletin_create.html',
                      {})

    def post(self, request: WSGIRequest):
        kw = fromRequest(request)
        kw['starterUser'] = request.user
        kw['starterAssociation'] = Association.objects.filter(founder=request.user, created=True).first()
        kw['title'] = '申请发布公告'
        kw['content'] = f'详细内容：{kw["bulletinMessage"][:20]}...'
        ba = BulletinApplication(**kw)
        ba.save()
        return render(request, 'big_info.html',
                      {'info': tInfo('申请已发送', '请耐心给等待教务员工审核。', href='/founder/app/list/3')})


def bulletins(request: WSGIRequest):
    ids = [a.id for a in Association.objects.filter(founder=request.user).all()]
    messages = BulletinApplication.objects.filter(result=1).exclude(starterAssociation_id__in=ids).all()
    return render(request, 'founder/bulletins.html',
                  {'messages': messages,
                   'assoc_id': assoc_id})
