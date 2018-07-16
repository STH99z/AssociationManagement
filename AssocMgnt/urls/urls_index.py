from django.urls import path, include
from AssocMgnt.views.index_views import *

urlpatterns = [
    path('', welcome),
    path('login/', login),
    path('logout/', logout),
]
