from django.urls import path
from AssocMgnt.views.test_views import *

urlpatterns = [
    path('top/', test_top),
    path('l1/', test_level1),
]
