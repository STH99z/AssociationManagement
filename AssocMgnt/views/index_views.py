from django.shortcuts import render
from django.http import HttpResponse
from AssocMgnt.template_models import *


# Create your views here.

def welcome(request):
    staff_login_modal = tModal(
        'staff_login_modal',
        title='教务员工登录',
        fields=[tModalField('uid1', text='员工号', name='uid'),
                tModalField('password1', text='密码', type='password', name='password')],
        buttons=[tSubmitButton(text='登录'),
                 tButton(text='取消', btn_class='btn-red')]
    )
    founder_login_modal = tModal(
        'founder_login_modal',
        title='社团负责人登录',
        fields=[tModalField('uid2', text='学号', name='uid'),
                tModalField('password2', text='密码', type='password', name='password')],
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


def test_top(request):
    return render(request, 'top.html', context={})
