from django.urls import path
from django.http import HttpResponseRedirect
from AssocMgnt.views import render
from AssocMgnt.views.staff_views import *


def empty_view(request, *args, **kwargs):
    return render(request, 'level1.html', kwargs)


def redirect(url):
    def view(request):
        return HttpResponseRedirect(url)

    return view


urlpatterns = [
    path(r'', redirect('/staff/assoc/list/')),
    path(r'assoc/list/', assoc_list),
    path(r'assoc/<int:assoc_id>/', assoc_id),
    path(r'assoc/<int:assoc_id>/bulletin/', assoc_id_bulletin),
    path(r'assoc/<int:assoc_id>/dismiss/', assoc_id_dismiss),  # class
    path(r'app/list/', app_list),
    path(r'app/list/<int:app_type>/', app_list),
    path(r'app/<int:app_id>/', app_id),  # class
    path(r'app/<int:app_id>/export/', app_id_export),
]
