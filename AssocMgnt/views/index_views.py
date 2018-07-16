from . import render
from django.http import HttpResponse, HttpResponseRedirect
from AssocMgnt.template_models import *
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.gzip import gzip_page
from logging import getLogger

logger = getLogger(__name__)


@gzip_page
def welcome(request: WSGIRequest):
    staff_login_modal = tModal(
        'staff_login_modal',
        action='login/',
        title='教务员工登录',
        fields=[tModalField('uid1', text='员工号', name='uid'),
                tModalField('password1', text='密码', type='password', name='password'),
                tModalField('', type='hidden', text='1', name='role'), ],
        buttons=[tSubmitButton(text='登录'),
                 tButton(text='取消', btn_class='btn-red')]
    )
    founder_login_modal = tModal(
        'founder_login_modal',
        action='login/',
        title='社团负责人登录',
        fields=[tModalField('uid2', text='学号', name='uid'),
                tModalField('password2', text='密码', type='password', name='password'),
                tModalField('', type='hidden', text='0', name='role'), ],
        buttons=[tSubmitButton(text='登录'),
                 tButton(text='取消', btn_class='btn-red')]
    )
    staff_login_button = tAButton(text='教师登录', data_target='staff_login_modal', data_toggle='modal')
    founder_login_button = tAButton(text='社团负责人登录', data_target='founder_login_modal', data_toggle='modal')
    context = {
        'staff_login_button': staff_login_button,
        'founder_login_button': founder_login_button,
        'staff_login_modal': staff_login_modal,
        'founder_login_modal': founder_login_modal,
    }
    return render(request, 'welcome.html', context=context)


@gzip_page
def login(request: WSGIRequest):
    from AssocMgnt.models import User
    from django.contrib.auth import authenticate, \
        login as auth_login, \
        logout as auth_logout
    uid = request.POST['uid']
    pwd = request.POST['password']
    role = request.POST['role']
    user = User.objects.filter(uid=uid, role=role).first()
    logger.info('retrieve user = %s' % user)
    if user is None:
        info = tInfo(palette='warning', title='登录失败！', text='你可能输入了错误的uid或密码，请返回重试！', icon='warning')
        return render(request, 'big_info.html', {'info': info})
    auth_user = authenticate(username=user.username, password=pwd)
    if user == auth_user:
        auth_logout(request)
        auth_login(request, auth_user)
        # TODO 2018/7/16 9:53: 根据用户重定向到staff和founder的url
        if user.role == User.ROLE_FOUNDER:
            return HttpResponseRedirect('/founder/assoc/list')
        elif user.role == User.ROLE_STAFF:
            return HttpResponseRedirect('/staff')
    info = tInfo(palette='warning', title='登录失败！', text='你可能输入了错误的uid或密码，请返回重试！', icon='warning')
    return render(request, 'big_info.html', {'info': info})


@gzip_page
def logout(request: WSGIRequest):
    from django.contrib.auth import logout as auth_logout
    user = request.user
    if user is None:
        return HttpResponseRedirect('/')
    auth_logout(request)
    return render(request, 'big_info.html', {'info': tInfo(title='您已退出登录', text='请点击按钮回到主页')})
