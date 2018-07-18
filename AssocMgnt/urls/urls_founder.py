from django.urls import path
from AssocMgnt.views import render
from AssocMgnt.views.founder_views import *


def empty_view(request, *args, **kwargs):
    return render(request, 'level1.html', kwargs)


urlpatterns = [
    path(r'assoc/list/', assoc_list),
    path(r'assoc/<int:assoc_id>/', assoc_id),
    path(r'assoc/<int:assoc_id>/edit/', assoc_id_edit.as_view()),
    path(r'assoc/<int:assoc_id>/members/', assoc_id_members.as_view()),
    path(r'assoc/<int:assoc_id>/bulletin/', assoc_id_bulletin.as_view()),
    path(r'app/list/<int:app_type>/', app_list),
    path(r'app/list/', app_list),
    path(r'app/<int:app_id>/', app_id),
    path(r'app/assoc/create/', app_assoc_create.as_view()),
    path(r'app/bulletin/create/', app_bulletin_create.as_view()),
    path(r'app/event/create/', app_event_create.as_view()),
    path(r'app/location/create/', app_location_create.as_view()),
    path(r'bulletins/', bulletins),
]
