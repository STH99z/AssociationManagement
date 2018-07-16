from django.core.handlers.wsgi import WSGIRequest
from AssocMgnt.models import *
from AssocMgnt.template_models import *
from . import render


def assoc_list(request: WSGIRequest):
    user = request.user
    assoc_list = Association.objects.filter(founder=user).all()
    button = tAButton(text='申请创建社团', href='/founder/app/assoc/create')
    return render(request, 'assoc_list.html', {'assoc_list': assoc_list,
                                               'button': button})
