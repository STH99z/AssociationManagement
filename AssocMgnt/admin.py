from django.contrib import admin

# Register your models here.
from AssocMgnt.models import *

admin.site.register(User)
admin.site.register(StuffPermission)
admin.site.register(Association)
admin.site.register(Member)
admin.site.register(Location)
admin.site.register(RegistrationApplication)
admin.site.register(EventApplication)
admin.site.register(LocationApplication)
admin.site.register(BulletinApplication)
