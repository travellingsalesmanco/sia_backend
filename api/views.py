# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


###------------------------------ PROFILE VIEWS --------------------------------------------------------------------####
#Request with username
class TechnicianProfile(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.filter(userID=username)
        #serialised_queryset = <serialiser>
        return Response(serialised_queryset)

#Request with username
class OtherProfile(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.filter(userID=username)
        # serialised_queryset = <serialiser>
        return Response(serialised_queryset)

##------------------------------- GENERAL APIS -------------------------------------------------------------##
#Request with id
class TechProfilefromID:
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.filter(userID=username)
        # serialised_queryset = <serialiser>
        return Response(serialised_queryset)

#Request with id
class DefectInfofromID:
    def get(self, request, format=None):
        defect_id = request.data["id"]
        queryset = Defects.objects.filter(id=defect_id)
        # serialised_queryset = <serialiser>
        return Response(serialised_queryset)

#------------------------------- SUPERVISOR/PLANNER APIS -------------------------------------------------------------##

class TechnicianList(APIView):
    def get(self, request, format=None):
        queryset = Profile.objects.filter(user_type=2)
        #serialised_queryset = <serialiser>
        return Response(serialised_queryset)


class AllDefects(APIView):
    def get(self, request, format=None):
        queryset = Defects.objects.filter(closed=false)
        # serialised_queryset = <serialiser>
        return Response(serialised_queryset)


# ------------------------------- TECHNICIAN APIS -------------------------------------------------------------##


#Request with username, return all defects associated with username
class TechnicianDefects(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Defects.objects.filter(techs_assigned__userID=username, closed=false)
        #serialised_queryset = <serialiser>
        return Response(serialised_queryset)

#Request with username, lon, lat
class TechUpdateLocation:
    def post(self, request, format=None):
        lon = request.data.get('lon')
        lat = request.data.get('lat')
        username = request.data.get('username')
        technician = Profile.objects.get(name=username)
        technician.lon = lon
        technician.lat = lat
        technician.save()
        return Response({'received data': request.data})

#def techUpdate():

#def supUpdate():

#def plannerUpdate():