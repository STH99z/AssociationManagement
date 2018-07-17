def tModal(_id, **kwargs):
    d = {'id': _id,
         'title': '模态框标题',
         'fields': list(),
         'buttons': list(),
         }.copy()
    d.update(kwargs)
    return d


def tModalField(_id, **kwargs):
    d = {'type': 'text',
         'id': _id,
         'data_success': '',
         'data_error': '不合法',
         'for': '',
         'text': '模态框 域',
         'name': _id,
         }.copy()
    d.update(kwargs)
    return d


def tButton(**kwargs):
    d = {'btn_class': 'btn-primary',
         'text': '按钮标题',
         'data_toggle': '',
         'data_target': '',
         'data_dismiss': 'modal',
         }.copy()
    d.update(kwargs)
    return d


def tAButton(**kwargs):
    d = tButton(**kwargs)
    d.update(tag='a', href='#')
    d.update(**kwargs)
    return d


def tSubmitButton(**kwargs):
    d = tButton(**kwargs)
    d.update(tag='submit')
    d.update(**kwargs)
    return d


def tInfo(title='标题', text='显示文本', **kwargs):
    d = {'title': title,
         'text': text,
         'icon': 'info-circle',
         'palette': 'primary',
         'href': '/',
         }.copy()
    d.update(kwargs)
    return d


if __name__ == '__main__':
    staffLoginModal = tModal(
        'staffLoginModal',
        title='教务员工登录',
        fields=[tModalField('uid', text='员工号'),
                tModalField('password', text='密码')],
        buttons=[tButton(text='登录'),
                 tButton(text='取消')]
    )
    print(staffLoginModal)
