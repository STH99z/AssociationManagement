from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from AssocMgnt.models import *
from AssocMgnt.template_models import *
from . import render
from django.template import Template, Engine, Context
from django.shortcuts import get_list_or_404, get_object_or_404
import logging

engine = Engine.get_default()
logger = logging.getLogger(__name__)


def assoc_list(request: WSGIRequest):
    user = request.user
    assoc_list = Association.objects.filter(founder=user, created=True).all()
    button = tAButton(text='申请创建社团', href='/founder/app/assoc/create')
    return render(request, 'founder/assoc_list.html',
                  {'assoc_list': assoc_list,
                   'button': button})


def assoc_id(request: WSGIRequest):
    return render(request, 'level1_founder.html', {})


class assoc_id_edit(View):
    def get(self, request: WSGIRequest, assoc_id: int):
        return render(request, 'level1_founder.html', {})

    def post(self, request: WSGIRequest, assoc_id: int):
        return render(request, 'level1_founder.html', {})


def assoc_id_members(request: WSGIRequest, assoc_id: int):
    return render(request, 'level1_founder.html', {})


def assoc_id_bulletin(request: WSGIRequest, assoc_id: int):
    return render(request, 'level1_founder.html', {})


def app_list(request: WSGIRequest):
    return render(request, 'level1_founder.html', {})


def app_id(request: WSGIRequest, app_id: int):
    return render(request, 'level1_founder.html', {})


class app_assoc_create(View):
    def get(self, request: WSGIRequest):
        user = request.user
        registerd_assoc_list = Association.objects.filter(created=True).all()
        return render(request, 'founder/assoc_create.html', {'registerd_assoc_list': registerd_assoc_list})

    def post(self, request: WSGIRequest):
        kw = dict(request.POST)
        kw['founder'] = request.user
        kw['parent'] = Association.objects.filter(id=request.POST.get('parent', '-1')).first()
        kw.pop('csrfmiddlewaretoken')
        logger.info(kw)
        a = Association(**kw)
        a.save()
        b = RegistrationApplication.create_one(request.user, None, a)
        b.save()
        return render(request, 'big_info.html',
                      {'info': tInfo(title='申请已发送', text='请耐心给等待教务员工审核。', href='')})


class app_event_create(View):
    def get(self, request: WSGIRequest):
        return render(request, 'level1_founder.html', {})


class app_location_create(View):
    def get(self, request: WSGIRequest):
        return render(request, 'level1_founder.html', {})


class app_bulletin_create(View):
    def get(self, request: WSGIRequest):
        return render(request, 'level1_founder.html', {})


def bulletins(request: WSGIRequest):
    return render(request, 'level1_founder.html', {})
