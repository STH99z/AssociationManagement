from . import render
from AssocMgnt.models import User
from django.core.handlers.wsgi import WSGIRequest
from . import *


@require_role(User.ROLE_STAFF)
def test_top(request: WSGIRequest):
    return render(request, 'top.html', context={})


def test_level1(request: WSGIRequest):
    return render(request, 'level1.html', context={})
