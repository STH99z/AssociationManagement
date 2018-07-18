from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import DO_NOTHING, SET_NULL, SET_DEFAULT, CASCADE
from django.utils.timezone import datetime, timedelta


# Create your models here.

class User(AbstractUser):
    ROLE_FOUNDER = 0
    ROLE_STAFF = 1
    ROLE_ADMIN = 2
    ROLES = (
        (ROLE_FOUNDER, '社团创立者'),
        (ROLE_STAFF, '教务员工'),
        (ROLE_ADMIN, '系统管理员')
    )
    ROLES_TEXT = {
        0: 'founder',
        1: 'staff',
        2: 'admin',
    }

    uid = models.CharField(max_length=16, null=False, verbose_name='学号/员工号')
    realName = models.CharField(max_length=32, null=True, blank=True, verbose_name='真实姓名')
    role = models.IntegerField(choices=ROLES, default=0, verbose_name='角色')
    tel = models.CharField(max_length=48, null=True, blank=True, verbose_name='联系电话')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    def __str__(self):
        return f'{User.ROLES[self.role][1]} {self.uid}'

    class Meta:
        verbose_name_plural = verbose_name = '用户'
        db_table = 'user'

    @property
    def role_text(self):
        return self.ROLES_TEXT[self.role]

    @staticmethod
    def create_phone():
        import random
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137",
                   "138", "139", "147", "150", "151", "152", "153", "155",
                   "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    @staticmethod
    def create_founders():
        from django.contrib.auth.hashers import make_password
        User.objects.filter(role=User.ROLE_FOUNDER).delete()
        for i in range(1, 31):
            uid = '15124802' + '%02i' % i
            pwd = uid
            user = User(uid=uid, password=make_password(pwd), role=User.ROLE_FOUNDER, tel=create_phone(),
                        username='User' + uid)
            user.save()
            print(user.username)

    @staticmethod
    def create_staffs():
        from django.contrib.auth.hashers import make_password
        User.objects.filter(role=User.ROLE_STAFF).delete()
        for i in range(1, 6):
            uid = 'S' + '%02i' % i
            pwd = uid + uid
            user = User(uid=uid, password=make_password(pwd), role=User.ROLE_STAFF, tel=create_phone(),
                        username='Staff' + uid)
            user.save()
            perm = StaffPermission(staff=user)
            perm.save()
            print(user.username)


class StaffPermission(models.Model):
    staff = models.ForeignKey(User, on_delete=CASCADE, db_column='staff', related_name='staff', verbose_name='教务员工')
    registration_perm = models.BooleanField(verbose_name='注册审核权', default=False, null=False)
    event_perm = models.BooleanField(verbose_name='活动审核权', default=False, null=False)
    location_perm = models.BooleanField(verbose_name='场所审核权', default=False, null=False)
    bulletin_perm = models.BooleanField(verbose_name='公告审核权', default=False, null=False)

    class Meta:
        verbose_name_plural = verbose_name = '教务员工权限'
        db_table = 'perm'

    def __str__(self):
        return f'{self.staff.uid} 权限: ' \
               f'R{"√" if self.registration_perm else "×"} ' \
               f'E{"√" if self.event_perm else "×"} ' \
               f'L{"√" if self.location_perm else "×"} ' \
               f'B{"√" if self.bulletin_perm else "×"}'


class Association(models.Model):
    name = models.TextField(max_length=128, null=False, verbose_name='社团名称')
    founder = models.ForeignKey(User, on_delete=CASCADE, db_column='founder', related_name='founder',
                                verbose_name='创立者')
    introduction = models.TextField(verbose_name='简介', blank=True)
    parent = models.ForeignKey('self', on_delete=DO_NOTHING, db_column='parent_assoc', related_name='parent_assoc',
                               verbose_name='父级社团', blank=True, null=True, default=None)
    created = models.BooleanField(verbose_name='是否已创建', default=False)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True)
    credit = models.IntegerField(default=100, null=False, verbose_name='信用点数', blank=True)
    deletionMark = models.BooleanField(default=False, verbose_name='解散标记', blank=True)
    deletionReason = models.TextField(null=True, verbose_name='解散原因', blank=True)
    deletionTime = models.DateTimeField(null=True, verbose_name='解散倒计时', blank=True)

    def __str__(self):
        return f'社团 {self.name}'

    class Meta:
        verbose_name = verbose_name_plural = '社团'
        db_table = 'association'

    @property
    def is_valid(self):
        return datetime.now() < self.deletionTime

    def update(self, **kwargs):
        import logging
        updated = {}
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
                updated[k] = v
        logging.getLogger(__name__).info(updated)


class Member(models.Model):
    association = models.ForeignKey(Association, on_delete=CASCADE, db_column='association', related_name='association',
                                    verbose_name='社团')
    name = models.CharField(max_length=32, null=False, verbose_name='姓名')
    tel = models.CharField(max_length=48, null=False, verbose_name='联系电话')

    def __str__(self):
        return f'社团 {self.association.name} 成员 {self.name} 联系电话 {self.tel}'

    class Meta:
        verbose_name_plural = verbose_name = '社团成员'
        db_table = 'member'


class Location(models.Model):
    name = models.TextField(verbose_name='地点名')
    where = models.TextField(max_length=128, verbose_name='具体位置', null=True, blank=True)

    def __str__(self):
        return f'{self.name} 详细位置：{self.where}'

    class Meta:
        verbose_name_plural = verbose_name = '地点'
        db_table = 'location'
        ordering = ['-name']


class ApplicationRecord(models.Model):
    APPLICATION_RESULTS = (
        (0, '待审核'),
        (1, '审核通过'),
        (2, '审核未通过'),
    )

    APPLICATION_NOTICED = (
        (False, '未阅'),
        (True, '已阅'),
    )

    class_name = 'ApplicationRecord'

    def __str__(self):
        return f'{"%04i" % self.id} {self.title} ' \
               f'发起社团：{self.starterAssociation.name if self.starterAssociation is not None else "无"}'

    title = models.TextField(max_length=32, verbose_name='申请标题')
    content = models.TextField(verbose_name='申请内容')
    starterUser = models.ForeignKey(User, on_delete=DO_NOTHING, null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_starter_user',
                                    verbose_name='申请人')
    starterAssociation = models.ForeignKey(Association, on_delete=CASCADE, null=True, blank=True, default=None,
                                           verbose_name='申请社团')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    result = models.IntegerField(choices=APPLICATION_RESULTS, default=0, verbose_name='审核结果')
    suggestion = models.TextField(verbose_name='审核意见', null=True, blank=True, default=None)
    reviewer = models.ForeignKey(User, on_delete=DO_NOTHING, related_name='%(app_label)s_%(class)s_reviewer',
                                 verbose_name='审核人', null=True, blank=True, default=None)
    reviewTime = models.DateTimeField(verbose_name='审核时间',
                                      auto_now=True, null=True, blank=True)
    noticed = models.BooleanField(default=False, null=False, verbose_name='学生已阅')

    class Meta:
        verbose_name = verbose_name_plural = '申请'
        abstract = True

    def update(self, **kwargs):
        import logging
        updated = {}
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
                updated[k] = v
        logging.getLogger(__name__).info(updated)

    @property
    def app_type(self):
        types = [RegistrationApplication, EventApplication, LocationApplication, BulletinApplication]
        for i, t in enumerate(types):
            if isinstance(self, t):
                return i
        return -1


class RegistrationApplication(ApplicationRecord):
    association = models.ForeignKey(Association, on_delete=DO_NOTHING, related_name='register_assoc',
                                    verbose_name='申请注册社团')

    class_name = 'RegistrationApplication'

    @classmethod
    def create_one(cls, starter_user, starter_assoc, association):
        app = RegistrationApplication(title='申请注册社团',
                                      content=f'申请注册名为“{association.name}”的社团。',
                                      starterUser=starter_user,
                                      starterAssociation=starter_assoc,
                                      association=association)
        return app

    class Meta:
        verbose_name = verbose_name_plural = '社团注册申请'
        db_table = 'registration_app'


class EventApplication(ApplicationRecord):
    class_name = 'EventApplication'
    OFFICIAL_HOLDING = (
        (False, '非官方'),
        (True, '官方'),
    )
    HOLDING_STATUS = (
        (False, '未举办'),
        (True, '已举办'),
    )
    USING_LOCATION = (
        (False, '使用其他地点'),
        (True, '使用校内地点'),
    )

    name = models.TextField(default='', verbose_name='活动名称')
    official = models.BooleanField(choices=OFFICIAL_HOLDING, default=False, verbose_name='是否为校方举办')
    fromTime = models.DateTimeField(verbose_name='开始时间')
    toTime = models.DateTimeField(verbose_name='结束时间')
    confirmHeld = models.BooleanField(choices=HOLDING_STATUS, verbose_name='是否已举办', default=False)
    holdingTime = models.DateTimeField(verbose_name='实际举办时间', null=True, blank=True, default=None)
    useLocation = models.BooleanField(choices=USING_LOCATION, default=True, verbose_name='使用校内地点')
    locationApplication = models.ForeignKey('LocationApplication', on_delete=DO_NOTHING, null=True, blank=True,
                                            default=None,
                                            db_column='loc_app', related_name='loc_app', verbose_name='场所使用申请')

    class Meta:
        verbose_name = verbose_name_plural = '活动申请'
        db_table = 'event_app'


class LocationApplication(ApplicationRecord):
    class_name = 'LocationApplication'
    LOCATION_SHARING = (
        (False, '独占'),
        (True, '共用'),
    )

    fromTime = models.DateTimeField(verbose_name='开始时间')
    toTime = models.DateTimeField(verbose_name='结束时间')
    location = models.ForeignKey(Location, on_delete=DO_NOTHING, db_column='location', related_name='location',
                                 verbose_name='地点')
    shareLocation = models.BooleanField(choices=LOCATION_SHARING, default=False, null=False, verbose_name='共用地点')

    class Meta:
        verbose_name = verbose_name_plural = '场所申请'
        db_table = 'location_app'


class BulletinApplication(ApplicationRecord):
    class_name = 'BulletinApplication'
    bulletinMessage = models.TextField()

    class Meta:
        verbose_name = verbose_name_plural = '公告发布申请'
        db_table = 'bulletin_app'
