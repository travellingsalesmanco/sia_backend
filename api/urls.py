from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from api import views as api_views

urlpatterns = [
#GET REQUESTS
    url(r'^auth$', drf_views.obtain_auth_token, name='auth'),
    url(r'^gettech$', api_views.TechnicianProfile.as_view(), name='techprofile'),
    url(r'^getuser$', api_views.OtherProfile.as_view(), name='profile'),


    url(r'^defects$', api_views.AllDefects.as_view(), name='alldefects'),
    url(r'^techs$', api_views.TechnicianList.as_view(), name='alltechs'),

    url(r'^defect$', api_views.DefectInfofromID.as_view(), name='defectinfo'),
    url(r'^tech$', api_views.TechProfilefromID.as_view(), name='techinfo'),

    url(r'^techdefects$', api_views.TechnicianDefects.as_view(), name='techdefects'),
    url(r'^techhistory$', api_views.TechnicianHistory.as_view(), name='techhistory'),

#POST REQUESTS
    url(r'^createdefect$', api_views.CreateOrUpdateDefect.as_view(), name='createdefect'),

#PATCH REQUESTS
    url(r'^updatedefect/(?P<pk>[0-9]+)$', api_views.CreateOrUpdateDefect.as_view(), name='updatedefect'),

#PUT/DELETE REQUESTS
    url(r'^update/(?P<pk>[0-9]+)$', api_views.AddOrDeleteUpdate.as_view(), name='update'),
    url(r'^spare/(?P<pk>[0-9]+)$', api_views.AddOrDeleteSpare.as_view(), name='spare'),
    url(r'^techassign/(?P<pk>[0-9]+)$', api_views.AddOrDeleteTechnician.as_view(), name='techassign'),
]
