from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from api import views as api_views

urlpatterns = [
#GET REQUESTS
    url(r'^auth$', drf_views.obtain_auth_token, name='auth'),
    url(r'^user/(?P<pk>[0-9]+)$', api_views.OtherProfileDetail.as_view(), name='profilelist'),
    url(r'^users$', api_views.OtherProfileList.as_view(), name='profiledetail'),

    url(r'^defects$', api_views.DefectsList.as_view(), name='defectsList'),
    url(r'^defect/(?P<pk>[0-9]+)$', api_views.DefectDetail.as_view(), name='defectinfo'),
    url(r'^createdefect$', api_views.DefectsList.as_view(), name='createdefect'),


    url(r'^techs$', api_views.TechnicianList.as_view(), name='alltechs'),

    url(r'^tech/(?P<pk>[0-9]+)$', api_views.TechDetail.as_view(), name='techinfo'),

    url(r'^techdefects$', api_views.TechnicianDefects.as_view(), name='techdefects'),
    url(r'^techhistory$', api_views.TechnicianHistory.as_view(), name='techhistory'),

#POST REQUESTS

#PATCH REQUESTS

#PUT/DELETE REQUESTS
    url(r'^update/(?P<pk>[0-9]+)$', api_views.AddOrRemoveUpdate.as_view(), name='update'),
    url(r'^addsparetodefect/(?P<pk>[0-9]+)$', api_views.AddOrRemoveSpareDetail.as_view(), name='sparedetail'),
    url(r'^techassign/(?P<pk>[0-9]+)$', api_views.AddOrRemoveTechnician.as_view(), name='techassign'),
]
