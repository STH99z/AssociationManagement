from django.shortcuts import render
from AssocMgnt.models import User
from django.http import HttpRequest
from . import *
from AssocMgnt import logger


@require_role(User.ROLE_STAFF)
def test_top(request: HttpRequest):
    print(type(request))
    logger.info(type(request))
    return render(request, 'top.html', context={})
