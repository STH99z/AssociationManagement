from django.urls import path
from AssocMgnt.views import render
from AssocMgnt.views.founder_views import *


def empty_view(request, *args, **kwargs):
    return render(request, 'level1.html', kwargs)


urlpatterns = [
    path(r'assoc/list/', assoc_list),
    path(r'assoc/<int:assoc_id>/', empty_view),
    path(r'assoc/<int:assoc_id>/edit/', empty_view),
    path(r'assoc/<int:assoc_id>/members/', empty_view),
    path(r'assoc/<int:assoc_id>/bulletin/', empty_view),
    path(r'app/list/', empty_view),
    path(r'app/<int:app_id>/', empty_view),
    path(r'app/assoc/create/', empty_view),
    path(r'app/bulletin/create/', empty_view),
    path(r'app/event/create/', empty_view),
    path(r'app/location/create/', empty_view),
    path(r'bulletins/', empty_view),
]
