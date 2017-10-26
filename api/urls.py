from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from api import views as api_views

urlpatterns = [
#GET REQUESTS
    url(r'^auth$', drf_views.obtain_auth_token, name='auth'),
    url(r'^techprofile$', api_views.TechnicianProfile.as_view(), name='techprofile'),
    url(r'^profile$', api_views.OtherProfile.as_view(), name='profile'),


    url(r'^alldefects$', api_views.AllDefects.as_view(), name='alldefects'),
    url(r'^alltechs$', api_views.TechnicianList.as_view(), name='alltechs'),

    url(r'^defectinfo$', api_views.DefectInfofromID.as_view(), name='defectinfo'),
    url(r'^techinfo$', api_views.TechProfilefromID.as_view(), name='techinfo'),

    url(r'^techdefects$', api_views.TechnicianDefects.as_view(), name='defectinfo'),

#POST REQUESTS
    url(r'^createdefect$', api_views.CreateOrUpdateDefect.as_view(), name='createdefect'),
    url(r'^addupdate', api_views.AddUpdate.as_view(), name='addupdate'),
    url(r'^assigntech$', api_views.AssignTechnician.as_view(), name='assigntech'),

#PATCH REQUESTS
    url(r'^updatedefect/(?P<pk>[0-9]+)$', api_views.CreateOrUpdateDefect.as_view(), name='updatedefect'),
]
